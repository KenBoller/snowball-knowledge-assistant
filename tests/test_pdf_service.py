from services.pdf_service import extract_text_from_pdf


def test_pdf_service_import():
    assert callable(extract_text_from_pdf)