import uuid
from dataclasses import dataclass

from app.documents.domain.entities import DocumentStatus


@dataclass(frozen=True)
class UploadDocumentInput:
    filename: str
    content_type: str
    uploaded_by: uuid.UUID


@dataclass(frozen=True)
class UploadDocumentResult:
    document_id: uuid.UUID
    filename: str
    content_type: str
    status: DocumentStatus


@dataclass(frozen=True)
class ParseDocumentResult:
    document_id: uuid.UUID
    markdown: str
    status: DocumentStatus
