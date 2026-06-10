from openai import OpenAI
import ollama
from app.config import OPENAI_API_KEY
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


def generate_answer(question: str, context: str) -> str:
    if not OPENAI_API_KEY:
        return "LLM answer generation requires OPENAI_API_KEY to be configured."

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Snowball Knowledge Assistant. "
                    "Answer using only the provided context. "
                    "If the answer is not in the context, say you do not know. "
                    "Be concise and include source references when possible."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
    )

    return response.choices[0].message.content


def answer_question(question: str, result_count: int = 5) -> dict:
    chunks = retrieve_relevant_chunks(
        question=question,
        result_count=result_count,
    )

    context = build_context(chunks)

    if not context:
        return {
            "question": question,
            "answer": "No relevant information found.",
            "sources": [],
        }

    try:
        response = ollama.chat(
            model="llama3.1:latest",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Snowball Knowledge Assistant.\n"
                        "Answer ONLY using the provided context.\n"
                        "If the answer is not in the context, say "
                        "'I could not find that information in the uploaded documents.'"
                    ),
                },
                {
                    "role": "user",
                    "content": f"""
Question:
{question}

Context:
{context}
""",
                },
            ],
        )

        answer = response["message"]["content"]

    except Exception as e:
        answer = f"Error calling Ollama: {str(e)}"

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "filename": chunk.get("metadata", {}).get("filename"),
                "chunk_index": chunk.get("metadata", {}).get("chunk_index"),
                "distance": chunk.get("distance"),
            }
            for chunk in chunks
        ],
    }