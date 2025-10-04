from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import importlib

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
    try:
        # 1. 使用deep_translator代替googletrans进行翻译
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source=req.source, target=req.target)
        translated_text = translator.translate(req.text)
        
        # 2. カタカナ/漢字読みの処理（fugashi/MeCabを使用）
        import fugashi
        # 动态获取unidic_lite字典路径
        try:
            # 尝试获取unidic_lite的安装路径
            import unidic_lite
            dicdir = os.path.join(os.path.dirname(unidic_lite.__file__), "dicdir")
            tagger = fugashi.GenericTagger(f"-d {dicdir}")
        except Exception:
            # 如果获取路径失败，尝试不指定路径启动
            tagger = fugashi.GenericTagger()
        
        # 3. ローマ字変換（romkanを使用）
        import romkan
        romaji = romkan.to_hepburn(translated_text)  # ヘボン式に変換
        
        return {"text": translated_text, "romaji": romaji}
        
    except Exception as e:
        # 添加错误处理
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")
