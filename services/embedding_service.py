import hashlib
import math
import re

from openai import OpenAI

from app.config import EMBEDDING_DIMENSIONS, EMBEDDING_PROVIDER, OPENAI_API_KEY


def create_local_embedding(text: str) -> list[float]:
    vector = [0.0] * EMBEDDING_DIMENSIONS

    words = re.findall(r"\b\w+\b", text.lower())

    for word in words:
        hash_value = int(hashlib.sha256(word.encode("utf-8")).hexdigest(), 16)
        index = hash_value % EMBEDDING_DIMENSIONS
        vector[index] += 1.0

    magnitude = math.sqrt(sum(value * value for value in vector))

    if magnitude == 0:
        return vector

    return [value / magnitude for value in vector]


def create_openai_embedding(text: str) -> list[float]:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not configured.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )

    return response.data[0].embedding


def create_embedding(text: str) -> list[float]:
    if EMBEDDING_PROVIDER == "openai":
        return create_openai_embedding(text)

    return create_local_embedding(text)