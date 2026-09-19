from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "Ok"}



