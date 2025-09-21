from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Language Converter (FastAPI)")

class ConvertRequest(BaseModel):
    text: str
    source: str = "auto"
    target: str = "ja"

@app.post("/convert")
async def convert(req: ConvertRequest):
    # TODO: 接入翻译引擎 & 罗马音后处理
    # 现在返回示例结构，方便前端联调
    translated_text = f"[SIMULATED JP] {req.text}"
    romaji = "koko-wa-simulēto"  # placeholder
    return {"text": translated_text, "romaji": romaji}
