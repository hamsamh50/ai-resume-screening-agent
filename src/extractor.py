from pathlib import Path
import pymupdf
from docx import Document


def extract_pdf_text(file_path):
    """Extract text from a PDF file."""

    document = pymupdf.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_docx_text(file_path):
    """Extract text from a DOCX file."""

    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:
        text.append(paragraph.text)

    return "\n".join(text)


def extract_txt_text(file_path):
    """Extract text from a TXT file."""

    return Path(file_path).read_text(encoding="utf-8")


def extract_text(file_path):
    """
    Detect the file type and extract its text.
    Supports PDF, DOCX and TXT.
    """

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    elif extension == ".txt":
        return extract_txt_text(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )