from services.chunking_service import chunk_text


def test_chunk_text_creates_chunks():
    text = "a" * 2500

    chunks = chunk_text(text, chunk_size=1000, overlap=200)

    assert len(chunks) == 4
    assert chunks[0]["chunk_index"] == 0
    assert chunks[1]["chunk_index"] == 1
    assert chunks[2]["chunk_index"] == 2
    assert chunks[3]["chunk_index"] == 3


def test_chunk_text_empty_text_returns_empty_list():
    chunks = chunk_text("")

    assert chunks == []