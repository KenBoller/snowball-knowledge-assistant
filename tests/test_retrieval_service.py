from services.retrieval_service import retrieve_relevant_chunks


def test_retrieval_service_import():
    assert callable(retrieve_relevant_chunks)