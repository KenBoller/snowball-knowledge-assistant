from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import UPLOAD_DIR

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided.")

    file_extension = Path(file.filename).suffix.lower()

    if file_extension != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    document_id = str(uuid4())
    saved_filename = f"{document_id}_{file.filename}"
    saved_path = UPLOAD_DIR / saved_filename

    file_content = await file.read()

    with open(saved_path, "wb") as uploaded_file:
        uploaded_file.write(file_content)

    return {
        "message": "Document uploaded successfully.",
        "document_id": document_id,
        "original_filename": file.filename,
        "saved_filename": saved_filename,
        "saved_path": str(saved_path),
        "content_type": file.content_type,
        "size_bytes": len(file_content),
    }