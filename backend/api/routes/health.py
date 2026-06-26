"""
Health endpoints.
"""

from fastapi import APIRouter

from backend.models import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
)
async def health() -> HealthResponse:
    """
    Basic health endpoint.
    """
    return HealthResponse(status="healthy")