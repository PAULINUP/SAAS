from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from app.ingestion.uploader import save_upload
from app.core.qcore_engine import process_question

router = APIRouter(prefix="/api", tags=["QCore"])

class AnalyzeRequest(BaseModel):
    question: str
    file_paths: List[str]

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        path = await save_upload(file)  # retorna caminho salvo
        return {"file_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_question(req: AnalyzeRequest):
    return process_question(req.question, req.file_paths)
