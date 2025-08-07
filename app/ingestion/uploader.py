# app/ingestion/uploader.py
import os
from fastapi import UploadFile
from uuid import uuid4

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload(file: UploadFile):
    filename = file.filename
    ext = filename.lower().split(".")[-1]
    unique_name = f"{uuid4().hex}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        return file_path
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar o arquivo {filename}: {e}")
