"""
Health endpoints.
"""

from fastapi import APIRouter

from backend.llm import LLMClient
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
    llm_client = LLMClient()
    return HealthResponse(
        status="healthy",
        llm_provider=llm_client.provider,
        llm_model=llm_client.model,
        semantic_analysis_configured=llm_client.is_configured,
    )
