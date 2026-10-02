import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from doc_processor.models.job_processing import ProcessingJobStatus


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    filename: str
    created_at: datetime


class ProcessingStatusResponse(BaseModel):
    document_id: uuid.UUID
    status: ProcessingJobStatus
