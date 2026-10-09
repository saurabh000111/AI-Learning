import logging
from time import perf_counter
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from doc_processor.core.logging import request_id_context

REQUEST_ID_HEADER = "X-Request-ID"
logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid4())
        started_at = perf_counter()
        context_token = request_id_context.set(request_id)

        try:
            request.state.request_id = request_id

            response = await call_next(request)

            response.headers[REQUEST_ID_HEADER] = request_id
            duration_ms = (perf_counter() - started_at) * 1000
            logger.info(
                "HTTP request completed method=%s path=%s status_code=%s "
                "duration_ms=%.2f",
                request.method,
                request.url.path,
                response.status_code,
                duration_ms,
            )

            return response
        finally:
            request_id_context.reset(context_token)
