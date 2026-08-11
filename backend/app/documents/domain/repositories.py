
from abc import ABC, abstractmethod
import uuid

from .entities import Document

class DocumentRepository(Protocol):
    def add(self, document: Document) -> None:
        ...

    def get_by_id(
        self,
        document_id: uuid.UUID,
    ) -> Document | None:
        ...

    def update(self, document: Document) -> None:
        ...
