import uuid

from sqlalchemy.orm import Session

from app.documents.domain.entities import (
    Document,
    DocumentStatus,
)
from app.documents.domain.repositories import DocumentRepository
from app.shared.infrastructure.database.document import DocumentModel


class SqlAlchemyDocumentRepository(DocumentRepository):
    def __init__(self, database_session: Session) -> None:
        self._database_session = database_session

    def add(self, document: Document) -> None:
        document_model = DocumentModel(
            id=document.id,
            filename=document.filename,
            content_type=document.content_type,
            uploaded_by=document.uploaded_by,
            status=document.status,
        )

        self._database_session.add(document_model)

    def get_by_id(
        self,
        document_id: uuid.UUID,
    ) -> Document | None:
        document_model = self._database_session.get(
            DocumentModel,
            document_id,
        )

        if document_model is None:
            return None

        return self._to_domain(document_model)

    def update(self, document: Document) -> None:
        document_model = self._database_session.get(
            DocumentModel,
            document.id,
        )

        if document_model is None:
            return

        document_model.filename = document.filename
        document_model.content_type = document.content_type
        document_model.uploaded_by = document.uploaded_by
        document_model.status = document.status

    @staticmethod
    def _to_domain(
        document_model: DocumentModel,
    ) -> Document:
        return Document(
            id=document_model.id,
            filename=document_model.filename,
            content_type=document_model.content_type,
            uploaded_by=document_model.uploaded_by,
            status=document_model.status,
        )
