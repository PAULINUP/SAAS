from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List
from app.ingestion.uploader import save_upload
from app.core.qcore_engine import process_question
# evite importar módulos com "..." por enquanto

router = APIRouter(prefix="/api", tags=["QCore AI"])

class AnalyzeRequest(BaseModel):
    question: str
    file_paths: List[str]

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    path = await save_upload(file)
    return {"file_path": path}

@router.post("/analyze")
async def analyze_question(req: AnalyzeRequest):
    # Por enquanto, passe apenas caminhos (stub do core lida com isso)
    result = process_question(req.question, req.file_paths)
    return result
