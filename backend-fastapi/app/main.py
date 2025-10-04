from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

@app.post("/convert")
async def convert(req: ConvertRequest):
    # 1. 翻訳エンジンの統合（例：Google Translate APIを使用）
    from googletrans import Translator
    translator = Translator()
    translated_text = translator.translate(req.text, src=req.source, dest=req.target).text
    
    # 2. カタカナ/漢字読みの処理（fugashi/MeCabを使用）
    import fugashi
    tagger = fugashi.GenericTagger()
    # ... カタカナ変換の処理 ...
    
    # 3. ローマ字変換（romkanを使用）
    import romkan
    romaji = romkan.to_hepburn(translated_text)  # ヘボン式に変換
    
    return {"text": translated_text, "romaji": romaji}
