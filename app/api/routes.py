from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List
from app.ingestion.uploader import save_upload
from app.core.qcore_engine import process_question
from app.simulation.macro_handler import process_directories  # novo import

router = APIRouter(prefix="/api", tags=["QCore AI"])

class AnalyzeRequest(BaseModel):
    question: str
    pdf_path: str

class MacroAnalyzeRequest(BaseModel):
    dir_paths: List[str]

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    path = await save_upload(file)
    return {"file_path": path}

@router.post("/analyze")
async def analyze_question(request: AnalyzeRequest):
    result = process_question(request.question, request.pdf_path)
    return result

@router.post("/macro_analyze")
async def macro_analyze(req: MacroAnalyzeRequest):
    result = process_directories(req.dir_paths)
    return {"macro_result": result}