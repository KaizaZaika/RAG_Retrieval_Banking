from typing import BinaryIO
from uuid import UUID

from minio import Minio

from app.config import settings
from app.documents.domain.repositories import DocumentStorage


class MinioDocumentStorage(DocumentStorage):
    def __init__(self) -> None:
        self._client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )

        self._bucket_name = settings.minio_bucket_name

    def store_document(
        self,
        document_id: UUID,
        filename: str,
        file: BinaryIO,
        content_type: str,
    ) -> str:
        self._ensure_bucket_exists()

        object_name = f"{document_id}/{filename}"

        self._client.put_object(
            self._bucket_name,
            object_name,
            file,
            length=-1,
            part_size=10 * 1024 * 1024,
            content_type=content_type,
        )

        return object_name

    def _ensure_bucket_exists(self) -> None:
        if not self._client.bucket_exists(self._bucket_name):
            self._client.make_bucket(self._bucket_name)
