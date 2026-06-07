from typing import Any

import chromadb

from app.config import CHROMA_DIR

client = chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_or_create_collection(collection_name: str = "snowball_documents"):
    return client.get_or_create_collection(name=collection_name)


def add_chunks_to_collection(
    chunks: list[dict],
    document_id: str,
    filename: str,
    embeddings: list[list[float]],
    collection_name: str = "snowball_documents",
) -> int:
    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks must match number of embeddings.")

    collection = get_or_create_collection(collection_name)

    ids = []
    documents = []
    metadatas: list[dict[str, Any]] = []

    for chunk, embedding in zip(chunks, embeddings):
        chunk_id = f"{document_id}_chunk_{chunk['chunk_index']}"

        ids.append(chunk_id)
        documents.append(chunk["text"])
        metadatas.append(
            {
                "document_id": document_id,
                "filename": filename,
                "chunk_index": chunk["chunk_index"],
                "start_char": chunk["start_char"],
                "end_char": chunk["end_char"],
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    return len(ids)


def search_collection(
    query_embedding: list[float],
    collection_name: str = "snowball_documents",
    result_count: int = 5,
) -> dict:
    collection = get_or_create_collection(collection_name)

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=result_count,
        include=["documents", "metadatas", "distances"],
    )