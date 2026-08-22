from uuid import UUID

from pydantic import BaseModel


class UploadedDocumentResponse(BaseModel):
    id: UUID
    filename: str
    content_type: str
    uploaded_by: UUID
    status: str
    storage_key: str
