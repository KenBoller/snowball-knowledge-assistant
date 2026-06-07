from services.retrieval_service import retrieve_relevant_chunks


def build_context(chunks: list[dict]) -> str:
    if not chunks:
        return ""

    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        metadata = chunk.get("metadata", {})

        source_label = (
            f"Source {index}: "
            f"{metadata.get('filename', 'unknown file')}, "
            f"chunk {metadata.get('chunk_index', 'unknown')}"
        )

        context_parts.append(
            f"{source_label}\n{chunk.get('text', '')}"
        )

    return "\n\n---\n\n".join(context_parts)


def answer_question(question: str, result_count: int = 5) -> dict:
    chunks = retrieve_relevant_chunks(
        question=question,
        result_count=result_count,
    )

    context = build_context(chunks)

    return {
        "question": question,
        "answer": "RAG answer generation is not connected yet.",
        "context": context,
        "sources": [
            {
                "filename": chunk.get("metadata", {}).get("filename"),
                "chunk_index": chunk.get("metadata", {}).get("chunk_index"),
                "distance": chunk.get("distance"),
            }
            for chunk in chunks
        ],
    }