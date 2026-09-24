from doc_processor.core.error_codes import ErrorCode
from doc_processor.exceptions.base import AppException


class ExternalServiceError(AppException):
    def __init__(
        self,
        message: str = "An external service error occurred.",
    ) -> None:
        super().__init__(
            code=ErrorCode.EXTERNAL_SERVICE_ERROR,
            message=message,
        )


class ExternalServiceUnavailableError(AppException):
    def __init__(self) -> None:
        super().__init__(
            code=ErrorCode.EXTERNAL_SERVICE_UNAVAILABLE,
            message="An external service is temporarily unavailable.",
        )


class ExternalServiceTimeoutError(AppException):
    def __init__(self) -> None:
        super().__init__(
            code=ErrorCode.EXTERNAL_SERVICE_TIMEOUT,
            message="An external service request timed out.",
        )


class ExternalServiceRateLimitedError(AppException):
    def __init__(self) -> None:
        super().__init__(
            code=ErrorCode.EXTERNAL_SERVICE_RATE_LIMITED,
            message="The external service rate limit has been exceeded.",
        )