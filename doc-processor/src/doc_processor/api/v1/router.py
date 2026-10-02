from fastapi import APIRouter

from doc_processor.api.v1.routes import auth, documents, health

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.health_router, tags=["health"])
api_router.include_router(auth.auth_router, tags=["authentication"])
api_router.include_router(documents.router, tags=["documents"])
