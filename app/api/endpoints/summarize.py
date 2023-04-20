from fastapi import APIRouter, File, UploadFile

router = APIRouter()


@router.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    """
    Endpoint that accepts a PDF file via a POST request.
    """
    # contents = await file.read()
    # print(contents)
    print("Works")
    # Here you can write code to process the PDF file
    return {
        "filename": file.filename
    }
