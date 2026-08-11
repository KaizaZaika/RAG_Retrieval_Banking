import uuid 
from dataclasses import dataclass, field
from enum import Enum 
class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


@dataclass
class Document:
    filename: str
    content_type: str
    uploaded_by: uuid.UUID

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: DocumentStatus = DocumentStatus.UPLOADED
