"""
Scan endpoints.
"""

from fastapi import APIRouter

from backend.models import ScanRequest, ScanResponse

router = APIRouter(tags=["Scanning"])


@router.post(
    "/scan",
    response_model=ScanResponse,
    summary="Scan a Prompt",
)
async def scan_prompt(request: ScanRequest) -> ScanResponse:
    """
    Placeholder scan endpoint.

    The detection pipeline will be connected here later.
    """

    return ScanResponse(
        request_id=request.request_id,
        blocked=False,
        risk_score=0.0,
        risk_level="low",
        threats=[],
        processing_time_ms=0.0,
        message="Detection engine not implemented yet.",
    )