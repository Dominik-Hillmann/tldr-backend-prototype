from io import BytesIO
import nltk
import pdfplumber
import time
import openai

nltk.download('punkt')

from nltk import word_tokenize
from typing import List


def get_token_len(text: str) -> int:
    tokens = word_tokenize(text)
    return len(tokens)


def break_up_tokens(tokens: List[str], chunk_size: int, overlap_size: int) -> List[str]:
    if len(tokens) <= chunk_size:
        yield tokens
    else:
        chunk = tokens[:chunk_size]
        # First return the current chunk, then return the broken rest of all chunks.
        yield chunk
        yield from break_up_tokens(tokens[(chunk_size - overlap_size):], chunk_size, overlap_size)


def detokenize(tokenized_text: List[str]) -> str:
    prompt_text = " ".join(tokenized_text)
    detokenized_text = prompt_text.replace(" 's", "'s")
    return detokenized_text


def to_text_from_pdf(file_in_memory: BytesIO) -> str:
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
    return complete_text


def summarize_by_chatgpt(doc_text: str, max_num_tokens: int = 1000, overlap: int = 100) -> str:
    chunks = break_up_tokens(word_tokenize(doc_text), max_num_tokens, overlap)
    prompt_responses = []

    for chunk in chunks:
        # print(f"Number of tokens: {len(chunk)}.")
        prompt_request = "Summarize this paper: " + detokenize(chunk)
        messages = [{
            "role": "system", 
            "content": "This is text summarization."
        }, {
            "role": "user", 
            "content": prompt_request
        }]    

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        time.sleep(20)
        
        print(response)
        response_text = response["choices"][0]["message"]["content"]
        prompt_responses.append(response_text)

    summary = " ".join(prompt_responses)

    # Recursively summarize the text until we get a summary of fewer that a 1000 tokens.    
    if get_token_len(summary) > 1000:
        return summarize_by_chatgpt(summary)
    else:
        return summary
    

def query_doc_content(question: str) -> str:
    messages = [{
        "role": "system", 
        "content": "Please answer this questions about the text you summarized earlier. Do not " +
        "explain why you answer this way."
    }, {
        "role": "user", 
        "content": question
    }]    

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=.5,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    time.sleep(20)

    response_text = response["choices"][0]["message"]["content"]
    return response_text    
