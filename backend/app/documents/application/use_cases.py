from typing import BinaryIO

from app.documents.application.models import (
    UploadDocumentInput,
    UploadDocumentOutput,
)
from app.documents.domain.entities import Document
from app.documents.domain.repositories import DocumentStorage


class UploadDocuments:
    def __init__(
        self,
        document_storage: DocumentStorage,
    ) -> None:
        self._document_storage = document_storage

    def upload_document(
        self,
        document_input: UploadDocumentInput,
        file: BinaryIO,
    ) -> UploadDocumentOutput:

        document = Document(
            filename=document_input.filename,
            content_type=document_input.content_type,
            uploaded_by=document_input.uploaded_by,
        )

        storage_key = self._document_storage.store_document(
            document_id=document.id,
            filename=document.filename,
            file=file,
            content_type=document.content_type,
        )

        return UploadDocumentOutput(
            id=document.id,
            filename=document.filename,
            content_type=document.content_type,
            uploaded_by=document.uploaded_by,
            status=document.status.value,
            storage_key=storage_key,
        )
