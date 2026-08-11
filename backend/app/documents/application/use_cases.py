import uuid

from app.documents.application.models import (
    ParseDocumentResult,
    UploadDocumentInput,
    UploadDocumentResult,
)
from app.documents.domain.entities import Document, DocumentStatus
from app.documents.domain.exceptions import (
    DocumentNotFoundError,
    DocumentParsingError,
)
from app.documents.domain.repositories import DocumentRepository
from app.documents.domain.services import DocumentParser


class UploadDocument:
    def __init__(
        self,
        document_repository: DocumentRepository,
    ) -> None:
        self._document_repository = document_repository

    def upload_document(
        self,
        upload_request: UploadDocumentInput,
    ) -> UploadDocumentResult:
        document = Document(
            filename=upload_request.filename,
            content_type=upload_request.content_type,
            uploaded_by=upload_request.uploaded_by,
        )

        self._document_repository.add(document)

        return UploadDocumentResult(
            document_id=document.id,
            filename=document.filename,
            content_type=document.content_type,
            status=document.status,
        )


class ParseDocument:
    def __init__(
        self,
        document_repository: DocumentRepository,
        document_parser: DocumentParser,
    ) -> None:
        self._document_repository = document_repository
        self._document_parser = document_parser

    def parse_document(
        self,
        document_id: uuid.UUID,
        file_path: str,
    ) -> ParseDocumentResult:
        document = self._document_repository.get_by_id(document_id)

        if document is None:
            raise DocumentNotFoundError(
                f"Document {document_id} was not found."
            )

        document.status = DocumentStatus.PROCESSING
        self._document_repository.update(document)

        try:
            parsed_document = self._document_parser.parse(file_path)
        except Exception as error:
            document.status = DocumentStatus.FAILED
            self._document_repository.update(document)

            raise DocumentParsingError(
                f"Failed to parse document {document_id}."
            ) from error

        document.status = DocumentStatus.READY
        self._document_repository.update(document)

        return ParseDocumentResult(
            document_id=document.id,
            markdown=parsed_document.markdown,
            status=document.status,
        )
