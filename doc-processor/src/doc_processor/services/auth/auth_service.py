from doc_processor.core.security import hash_password
from doc_processor.exceptions import UserAlreadyExistsError
from doc_processor.models.user import User
from doc_processor.repositories.user_repository import UserRepository
from doc_processor.db.session import AsyncSession
from doc_processor.core.jwt import create_access_token
from doc_processor.core.security import verify_password
from doc_processor.exceptions.auth import InvalidCredentialsError

class AuthService:
    def __init__(self, user_repository: UserRepository, db_session: AsyncSession) -> None:
        self.user_repository = user_repository
        self.db_session = db_session

    async def register(self, email: str, password: str) -> User:
        async with self.db_session.begin():
            normalized_email = email.strip().lower()

            existing_user = await self.user_repository.get_by_email(normalized_email)
            if existing_user is not None:
                raise UserAlreadyExistsError()

            user = await self.user_repository.create(
                email=normalized_email,
                password_hash=hash_password(password),
            )

        # Leaving the block successfully commits; an exception rolls back.
        return user

    async def login(self, email: str, password: str,) -> str:
        normalized_email = email.strip().lower()

        user = await self.user_repository.get_by_email(
            normalized_email
        )

        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InvalidCredentialsError()

        access_token = create_access_token(user.id)

        return access_token