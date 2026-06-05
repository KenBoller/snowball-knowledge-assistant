from services.embedding_service import create_embedding


def test_embedding_service_import():
    assert callable(create_embedding)