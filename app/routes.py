from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os
from .converter import convert_pdf_pages_to_tiff

router = APIRouter()

@router.post("/convert/")
async def convert_pdf(
    file: UploadFile = File(...),
    pages: str = Form(...)
):
    try:
        os.makedirs("input_pdfs", exist_ok=True)
        os.makedirs("output_tiffs", exist_ok=True)

        file_path = f"input_pdfs/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Parse pages like "1,3,4" → [0,2,3]
        try:
            page_indices = [int(p.strip()) - 1 for p in pages.split(",") if p.strip().isdigit()]
        except:
            return JSONResponse({"error": "Invalid page format"}, status_code=400)

        output_files = convert_pdf_pages_to_tiff(file_path, "output_tiffs", page_indices)

        if not output_files:
            return JSONResponse({"error": "No valid pages to convert"}, status_code=400)

        return FileResponse(output_files[0], media_type="image/tiff", filename=os.path.basename(output_files[0]))

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
