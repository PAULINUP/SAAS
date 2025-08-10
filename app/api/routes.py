# app/api/routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from app.ingestion.uploader import save_upload

router = APIRouter(prefix="/api", tags=["QCore"])

class AnalyzeRequest(BaseModel):
    question: str
    file_paths: List[str]

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        path = await save_upload(file)
        return {"file_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze(req: AnalyzeRequest):
    try:
        # TODO: ligar seu engine real aqui
        result = {
            "resumo_executivo": f"Pergunta: {req.question} / {len(req.file_paths)} arquivo(s).",
            "detalhe_tecnico": "Stub de análise — troque pelo engine.",
            "cenarios_alternativos": ["A","B"],
            "recomendacoes": ["Coletar mais dados"],
            "explicabilidade": "Regras demo.",
            "confianca": 0.82,
            "entidades": ["demo1","demo2"],
            "limitacoes": "Modelo ainda não treinado."
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
