from fastapi import APIRouter, File, UploadFile
import pdfplumber
from app.api.utils import get_token_len, break_up_tokens, detokenize
from nltk import word_tokenize
from io import BytesIO
import openai
import tiktoken
from dotenv import load_dotenv
import os
import time
from app.api.models import example_summary

router = APIRouter()
load_dotenv()
openai_key = os.getenv("OPENAI_KEY")

@router.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    """
    Endpoint that accepts a PDF file via a POST request.
    """

    openai.api_key = openai_key

    file_in_memory = BytesIO(await file.read())
    with pdfplumber.open(file_in_memory) as pdf:
        pages = []
        num_tokens_page = []
        for i, page in enumerate(pdf.pages):
            text_in_page = page.extract_text()
            num_tokens = get_token_len(text_in_page)
            num_tokens_page.append(num_tokens)
            print(f"Number of tokens in page {i + 1}: {num_tokens}")
            pages.append(text_in_page)

    complete_text = ' '.join(pages)

    prompt_response = []
    encoding = tiktoken.get_encoding("gpt2")

    chunks = break_up_tokens(word_tokenize(complete_text), 1000, 100)
    # for i, chunk in enumerate(chunks):
    #     # print(f"Number of tokens: {len(chunk)}.")
    #     prompt_request = "Summarize this paper: " + detokenize(chunk)
    #     messages = [{
    #         "role": "system", 
    #         "content": "This is text summarization."
    #     }, {
    #         "role": "user", 
    #         "content": prompt_request
    #     }]    

    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=messages,
    #         temperature=.5,
    #         max_tokens=500,
    #         top_p=1,
    #         frequency_penalty=0,
    #         presence_penalty=0
    #     )
        
    #     print(response)
    #     response_text = response["choices"][0]["message"]["content"]
    #     prompt_response.append(response_text)
    #     time.sleep(20)

    # print(f"Number 'pure' tokens: {sum(num_tokens_page)}")
    
    prompt_response = example_summary
    full_response_text = " ".join(prompt_response)
    print(prompt_response)

    return {
        "filename": file.filename,
        "text": pages
    }
