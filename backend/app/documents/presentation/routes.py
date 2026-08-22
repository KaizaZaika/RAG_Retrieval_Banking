from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from app.auth.presentation.dependencies import get_current_user
from app.documents.application.models import UploadDocumentInput
from app.documents.application.use_cases import UploadDocuments
from app.documents.domain.repositories import DocumentStorage
from app.documents.presentation.dependencies import get_document_storage
from app.documents.presentation.schemas import UploadedDocumentResponse


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=UploadedDocumentResponse,
)
async def upload_document(
    file: Annotated[
        UploadFile,
        File(description="Document to upload"),
    ],
    current_user=Depends(get_current_user),
    document_storage: DocumentStorage = Depends(
        get_document_storage
    ),
):
    upload_input = UploadDocumentInput(
        filename=file.filename or "unknown",
        content_type=file.content_type or "application/octet-stream",
        uploaded_by=current_user.id,
    )

    use_case = UploadDocuments(
        document_storage=document_storage,
    )

    uploaded_document = use_case.upload_document(
        document_input=upload_input,
        file=file.file,
    )

    return UploadedDocumentResponse(
        id=uploaded_document.id,
        filename=uploaded_document.filename,
        content_type=uploaded_document.content_type,
        uploaded_by=uploaded_document.uploaded_by,
        status=uploaded_document.status,
        storage_key=uploaded_document.storage_key,
    )
