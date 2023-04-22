from fastapi import APIRouter, File, UploadFile
import pdfplumber
from io import BytesIO

router = APIRouter()


@router.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    """
    Endpoint that accepts a PDF file via a POST request.
    """
    file_content = await file.read()
    file_in_memory = BytesIO(file_content)

    # print(contents)
    print("Works")

    with pdfplumber.open(file_in_memory) as pdf:
        first_page = pdf.pages[0]

    # Here you can write code to process the PDF file
    return {
        "filename": file.filename,
        "text": [ page.extract_text() for page in pdf.pages ]
    }
