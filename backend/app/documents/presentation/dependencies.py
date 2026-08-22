from app.documents.domain.repositories import DocumentStorage
from app.documents.infrastructure.minio_document_storage import (
    MinioDocumentStorage,
)


def get_document_storage() -> DocumentStorage:
    return MinioDocumentStorage()
