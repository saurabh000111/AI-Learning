from dataclasses import dataclass

from fastapi import status

from doc_processor.core.error_codes import ErrorCode


@dataclass(frozen=True)
class ErrorDefinition:
    status_code: int
    message: str


ERROR_DEFINITIONS: dict[ErrorCode, ErrorDefinition] = {
    ErrorCode.INTERNAL_ERROR: ErrorDefinition(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="An unexpected error occurred.",
    ),
    ErrorCode.VALIDATION_ERROR: ErrorDefinition(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Request validation failed.",
    ),
    ErrorCode.BAD_REQUEST: ErrorDefinition(
        status_code=status.HTTP_400_BAD_REQUEST,
        message="The request is invalid.",
    ),
    ErrorCode.AUTH_INVALID_CREDENTIALS: ErrorDefinition(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message="Invalid email or password.",
    ),
    ErrorCode.AUTH_USER_ALREADY_EXISTS: ErrorDefinition(
        status_code=status.HTTP_409_CONFLICT,
        message="User already exists.",
    ),
    ErrorCode.AUTH_USER_NOT_FOUND: ErrorDefinition(
        status_code=status.HTTP_404_NOT_FOUND,
        message="User not found.",
    ),
    ErrorCode.AUTH_UNAUTHORIZED: ErrorDefinition(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message="Authentication is required.",
    ),
    ErrorCode.FORBIDDEN: ErrorDefinition(
        status_code=status.HTTP_403_FORBIDDEN,
        message="You do not have permission to perform this operation.",
    ),
    ErrorCode.DB_ERROR: ErrorDefinition(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="A database error occurred.",
    ),
    ErrorCode.DB_INTEGRITY_ERROR: ErrorDefinition(
        status_code=status.HTTP_409_CONFLICT,
        message="The requested operation violates a database constraint.",
    ),
    ErrorCode.DB_UNAVAILABLE: ErrorDefinition(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        message="The database is temporarily unavailable.",
    ),
    ErrorCode.EXTERNAL_SERVICE_ERROR: ErrorDefinition(
        status_code=status.HTTP_502_BAD_GATEWAY,
        message="An external service error occurred.",
    ),
    ErrorCode.EXTERNAL_SERVICE_UNAVAILABLE: ErrorDefinition(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        message="An external service is temporarily unavailable.",
    ),
    ErrorCode.EXTERNAL_SERVICE_TIMEOUT: ErrorDefinition(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        message="An external service request timed out.",
    ),
    ErrorCode.EXTERNAL_SERVICE_RATE_LIMITED: ErrorDefinition(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        message="The external service rate limit has been exceeded.",
    ),
}