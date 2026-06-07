from services.embedding_service import create_embedding
from services.vector_service import search_collection


def retrieve_relevant_chunks(question: str, result_count: int = 5) -> list[dict]:
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    query_embedding = create_embedding(question)

    results = search_collection(
        query_embedding=query_embedding,
        result_count=result_count,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    chunks = []

    for document, metadata, distance in zip(documents, metadatas, distances):
        chunks.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return chunks