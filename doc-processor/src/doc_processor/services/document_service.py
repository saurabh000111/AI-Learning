import asyncio
import logging
import uuid

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from doc_processor.exceptions.database import DatabaseError
from doc_processor.models.documents import Document
from doc_processor.models.job_processing import ProcessingJob
from doc_processor.repositories.document_repository import DocumentRepository
from doc_processor.repositories.processing_job_repository import ProcessingJobRepository
from doc_processor.storage.local import delete_pdf, save_pdf

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(
        self,
        document_repository: DocumentRepository,
        session: AsyncSession,
        processing_job_repository: ProcessingJobRepository,
    ) -> None:
        self.document_repository = document_repository
        self.session = session
        self.processing_job_repository = processing_job_repository

    async def get_owned_document(
        self,
        document_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Document | None:
        return await self.document_repository.get_by_id_for_user(
            document_id,
            user_id,
        )

    async def delete_owned_document(
        self, document_id: uuid.UUID, user_id: uuid.UUID
    ) -> Document | None:
        """Deletes a document owned by a specific user.

        Args:
            document_id (uuid.UUID): The ID of the document to delete.
            user_id (uuid.UUID): The ID of the user who owns the document.

        Returns:
            Document | None: The deleted Document object if found and deleted, otherwise None.
        """

        try:
            document = await self.document_repository.delete_by_id_for_user(
                document_id, user_id
            )

            if document is not None:
                await self.session.commit()
                await asyncio.to_thread(delete_pdf, document_id)
                logger.info("Deleted document %s for user %s", document_id, user_id)

            return document
        except SQLAlchemyError as exc:
            logger.exception(
                "Database error while deleting document %s for user %s",
                document_id,
                user_id,
            )
            await self.session.rollback()
            raise DatabaseError() from exc

    async def list_owned_documents(
        self,
        user_id: uuid.UUID,
    ) -> list[Document]:
        """_summary_ Lists all documents owned by a specific user.

        Args:
            user_id (uuid.UUID): _description_

        Returns:
            list[Document]: _description_
        """
        return await self.document_repository.list_by_user(user_id)

    async def upload_document(
        self,
        user_id: uuid.UUID,
        filename: str,
        content: bytes,
    ) -> Document:
        """_summary_ Creates a new document record in the database and saves the PDF file to local storage.

        Args:
            user_id (uuid.UUID): _description_
            filename (str): _description_
            content (bytes): _description_

        Raises:
            DatabaseError: _description_

        Returns:
            Document: _description_
        """
        document_id = uuid.uuid4()

        # Try to save the PDF before attempting database INSERT
        try:
            filepath = await asyncio.to_thread(
                save_pdf,
                document_id,
                content,
            )

        except OSError:
            logger.exception("Failed to save PDF for document %s", document_id)
            raise

        try:
            document = await self.document_repository.create(
                document_id=document_id, user_id=user_id, filename=filename
            )

            job = await self.processing_job_repository.create(document_id=document_id)

            await self.session.commit()
            return document

        except Exception as exc:
            # Undo uncommitted database changes
            try:
                await self.session.rollback()
            except Exception:
                logger.exception(
                    "Database rollback failed for document %s", document_id
                )

            # Remove the PDF if database persistence fails.
            try:
                await asyncio.to_thread(filepath.unlink, missing_ok=True)
            except OSError:
                logger.exception("Failed to clean up PDF for document %s", document_id)

            if isinstance(exc, SQLAlchemyError):
                logger.exception(
                    "Database error while uploading document %s", document_id
                )
                raise DatabaseError() from exc

            raise

    async def get_owned_processing_job(
        self,
        document_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> ProcessingJob | None:
        document = await self.document_repository.get_by_id_for_user(
            document_id,
            user_id,
        )
        if document is None:
            return None

        return await self.processing_job_repository.get_by_document_id(document_id)
