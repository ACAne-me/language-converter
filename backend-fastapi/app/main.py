from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
import re
# 导入romkan库用于假名转罗马音
import romkan

# 配置日志记录\logging.basicConfig(level=logging.DEBUG)
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

# 导入中文名字映射模块
from app.name_mapping import get_japanese_pronunciation

@app.post("/convert")
async def convert(req: ConvertRequest):
    try:
        input_text = req.text.strip()
        if not input_text:
            raise HTTPException(status_code=400, detail="Empty input text")
            
        logger.debug(f"Received conversion request: {input_text}")
        
        # 定义中日文字符检测正则表达式
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        japanese_pattern = re.compile(r'[\u3040-\u309f\u30a0-\u30ff]')
        # 拉丁字母检测正则表达式
        latin_pattern = re.compile(r'[a-zA-Z]')
        
        # 判断是否包含中文字符
        has_chinese = bool(chinese_pattern.search(input_text))
        # 判断是否包含日文字符
        has_japanese = bool(japanese_pattern.search(input_text))
        # 判断是否包含拉丁字母
        has_latin = bool(latin_pattern.search(input_text))
        # 判断是否主要是拉丁字母（超过50%的字符是拉丁字母）
        is_latin_dominant = has_latin and (sum(1 for c in input_text if latin_pattern.match(c)) / len(input_text) > 0.5)
        
        translated_text = ""
        romaji = ""
        
        # 对于中文姓名的特殊处理（2-4个汉字）
        if has_chinese and not has_japanese and len(input_text) >= 2 and len(input_text) <= 4 and all(chinese_pattern.match(c) for c in input_text):
            logger.debug("Detected Chinese name, using name mapping")
            
            # 使用name_mapping模块进行翻译
            translated_text = get_japanese_pronunciation(input_text)
            # 使用romkan将假名转换为罗马音
            romaji = romkan.to_roma(translated_text)
        else:
            # 对于其他文本，使用deep_translator进行翻译
            from deep_translator import GoogleTranslator
            logger.debug("Using Google Translator for general text")
            
            try:
                # 对于主要是拉丁字母的输入，保持原始格式
                if is_latin_dominant:
                    translated_text = input_text
                    romaji = input_text
                else:
                    # 普通文本翻译
                    translator = GoogleTranslator(source=req.source, target=req.target)
                    translated_text = translator.translate(input_text)
                    # 对于非拉丁字母文本，罗马字暂时使用原文
                    romaji = translated_text
            except Exception as e:
                logger.error(f"Translation failed: {str(e)}")
                # 翻译失败时，使用原文作为备选
                translated_text = input_text
                romaji = input_text
        
        # 确保返回有意义的结果
        if not translated_text:
            translated_text = "Translation failed"
        if not romaji:
            romaji = ""
        
        return {"text": translated_text, "romaji": romaji}
        
    except Exception as e:
        logger.exception(f"Conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")
