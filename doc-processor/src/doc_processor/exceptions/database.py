from doc_processor.core.error_codes import ErrorCode
from doc_processor.exceptions.base import AppException


class DatabaseError(AppException):
    def __init__(
        self,
        message: str = "A database error occurred.",
    ) -> None:
        super().__init__(
            code=ErrorCode.DB_ERROR,
            message=message,
        )


class DatabaseIntegrityError(AppException):
    def __init__(
        self,
        message: str = "The requested operation violates a database constraint.",
    ) -> None:
        super().__init__(
            code=ErrorCode.DB_INTEGRITY_ERROR,
            message=message,
        )


class DatabaseUnavailableError(AppException):
    def __init__(self) -> None:
        super().__init__(
            code=ErrorCode.DB_UNAVAILABLE,
            message="The database is temporarily unavailable.",
        )