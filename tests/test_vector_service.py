from services.vector_service import (
    add_chunks_to_collection,
    get_or_create_collection,
    search_collection,
)


def test_vector_service_imports():
    assert callable(get_or_create_collection)
    assert callable(add_chunks_to_collection)
    assert callable(search_collection)