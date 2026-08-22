from abc import ABC, abstractmethod
from typing import BinaryIO
from uuid import UUID
from app.documents.domain.entities import Document


class DocumentRepository(ABC):

    @abstractmethod
    def add_document(self, document: Document) -> None:
        pass

class DocumentStorage(ABC):
    @abstractmethod
    def store_document(
        self,
        document_id: UUID,
        filename: str,
        file: BinaryIO,
        content_type: str,
    ) -> str:
        """Store a document and return its storage key."""
        raise NotImplementedError
