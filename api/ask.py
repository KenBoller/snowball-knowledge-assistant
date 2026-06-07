from fastapi import APIRouter
from pydantic import BaseModel
from services.vector_service import get_or_create_collection
from services.rag_service import answer_question

router = APIRouter(
    prefix="/ask",
    tags=["ask"],
)


class AskRequest(BaseModel):
    question: str
    result_count: int = 5


@router.post("")
def ask_question(request: AskRequest):
    return answer_question(
        question=request.question,
        result_count=request.result_count,
    )

@router.post("/debug")
def ask_debug(request: AskRequest):
    return answer_question(
        question=request.question,
        result_count=request.result_count,
    )

@router.get("/stats")
def stats():
    collection = get_or_create_collection()

    return {
        "documents_in_collection": collection.count()
    }