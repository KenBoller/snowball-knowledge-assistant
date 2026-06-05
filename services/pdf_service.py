from pathlib import Path

import fitz


def extract_text_from_pdf(pdf_path: str | Path) -> dict:
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("File must be a PDF.")

    pages = []

    with fitz.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text()

            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )

    full_text = "\n\n".join(page["text"] for page in pages)

    return {
        "file_path": str(path),
        "page_count": len(pages),
        "text_length": len(full_text),
        "pages": pages,
        "full_text": full_text,
    }