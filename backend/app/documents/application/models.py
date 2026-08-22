from dataclasses import dataclass
from uuid import UUID


@dataclass
class UploadDocumentOutput:
    id: UUID
    filename: str
    content_type: str
    uploaded_by: UUID
    status: str
    storage_key: str
@dataclass
class UploadDocumentInput:
    filename: str
    content_type: str
    uploaded_by: UUID
