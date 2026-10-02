import uuid
from pathlib import Path

from doc_processor.core.config import settings


def save_pdf(
    document_id: uuid.UUID,
    content: bytes,
) -> Path:
    """Save a validated PDF using its document ID."""

    upload_dir = settings.upload_dir
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / f"{document_id}.pdf"

    # Exclusive creation protects an existing document.
    with file_path.open("xb") as destination:
        try:
            destination.write(content)
        except OSError:
            # Close before deleting, including on Windows.
            destination.close()
            file_path.unlink(missing_ok=True)
            raise

    return file_path


def delete_pdf(document_id: uuid.UUID) -> None:
    """Delete a PDF file using its document ID."""
    upload_dir = settings.upload_dir
    file_path = upload_dir / f"{document_id}.pdf"

    file_path.unlink(missing_ok=True)


def get_pdf_path(document_id: uuid.UUID) -> Path:
    return settings.upload_dir / f"{document_id}.pdf"
