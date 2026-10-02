import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from doc_processor.models.documents import Document


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        document_id: uuid.UUID,
        user_id: uuid.UUID,
        filename: str,
    ) -> Document:
        document = Document(
            id=document_id,
            user_id=user_id,
            filename=filename,
        )

        self.session.add(document)

        await self.session.flush()
        await self.session.refresh(document)

        return document

    async def get_by_id_for_user(
        self,
        document_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Document | None:
        statement = select(Document).where(
            Document.id == document_id,
            Document.user_id == user_id,
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def delete_by_id_for_user(
        self,
        document_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Document | None:
        document = await self.get_by_id_for_user(document_id, user_id)

        if document is None:
            return None

        await self.session.delete(document)
        await self.session.flush()

        return document

    async def list_by_user(
        self,
        user_id: uuid.UUID,
    ) -> list[Document]:
        statement = (
            select(Document)
            .where(Document.user_id == user_id)
            .order_by(
                Document.created_at.desc(),
                Document.id.desc(),
            )
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all())
