import os, aiofiles
from fastapi import UploadFile

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload(file: UploadFile) -> str:
    dest = os.path.join(UPLOAD_DIR, file.filename)
    async with aiofiles.open(dest, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            await f.write(chunk)
    await file.close()
    return dest
