import nltk

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

