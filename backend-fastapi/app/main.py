from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
import re
# Import romkan library for kana to romaji conversion
import romkan

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("language-converter")

app = FastAPI(title="Language Converter (FastAPI)")

# CORS configuration - allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConvertRequest(BaseModel):
    text: str
    source: str = "auto"
    target: str = "ja"

# Import Chinese name mapping module
from app.name_mapping import get_japanese_pronunciation

@app.post("/convert")
async def convert(req: ConvertRequest):
    try:
        input_text = req.text.strip()
        if not input_text:
            raise HTTPException(status_code=400, detail="Empty input text")
            
        logger.debug(f"Received conversion request: {input_text}")
        
        # Define Chinese and Japanese character detection regex patterns
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        japanese_pattern = re.compile(r'[\u3040-\u309f\u30a0-\u30ff]')
        # Latin alphabet detection regex pattern
        latin_pattern = re.compile(r'[a-zA-Z]')
        
        # Check if contains Chinese characters
        has_chinese = bool(chinese_pattern.search(input_text))
        # Check if contains Japanese characters
        has_japanese = bool(japanese_pattern.search(input_text))
        # Check if contains Latin alphabet
        has_latin = bool(latin_pattern.search(input_text))
        # Check if primarily Latin alphabet (more than 50% of characters are Latin)
        is_latin_dominant = has_latin and (sum(1 for c in input_text if latin_pattern.match(c)) / len(input_text) > 0.5)
        
        translated_text = ""
        romaji = ""
        
        # Special handling for Chinese names (2-4 characters)
        if has_chinese and not has_japanese and len(input_text) >= 2 and len(input_text) <= 4 and all(chinese_pattern.match(c) for c in input_text):
            logger.debug("Detected Chinese name, using name mapping")
            
            # Use name_mapping module for translation
            translated_text = get_japanese_pronunciation(input_text)
            # Use romkan to convert kana to romaji
            romaji = romkan.to_roma(translated_text)
        else:
            # For other text, use deep_translator for translation
            from deep_translator import GoogleTranslator
            logger.debug("Using Google Translator for general text")
            
            try:
                # For primarily Latin input, keep original format
                if is_latin_dominant:
                    translated_text = input_text
                    romaji = input_text
                else:
                    # Normal text translation
                    translator = GoogleTranslator(source=req.source, target=req.target)
                    translated_text = translator.translate(input_text)
                    # For non-Latin text, temporarily use original text for romaji
                    romaji = translated_text
            except Exception as e:
                logger.error(f"Translation failed: {str(e)}")
                # If translation fails, use original text as fallback
                translated_text = input_text
                romaji = input_text
        
        # Ensure meaningful results are returned
        if not translated_text:
            translated_text = "Translation failed"
        if not romaji:
            romaji = ""
        
        return {"text": translated_text, "romaji": romaji}
        
    except Exception as e:
        logger.exception(f"Conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")
