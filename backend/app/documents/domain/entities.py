from dataclasses import dataclass, field
from enum import Enum
import uuid


class DocumentStatus(str, Enum):
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


@dataclass
class Document:
    filename: str
    content_type: str
    uploaded_by: uuid.UUID

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: DocumentStatus = DocumentStatus.UPLOADING
