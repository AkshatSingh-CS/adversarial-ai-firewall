"""
Scan API endpoints.

Receives prompts from clients and returns
structured detection results.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.detection.pipeline import DetectionPipeline
from backend.models.request_models import ScanRequest
from backend.models.response_models import ScanResponse

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/scan",
    tags=["Detection"],
)

# ============================================================
# Pipeline
# ============================================================

pipeline = DetectionPipeline()

# ============================================================
# Routes
# ============================================================

@router.post(
    "",
    response_model=ScanResponse,
    summary="Scan a prompt for adversarial attacks",
)
async def scan_prompt(
    request: ScanRequest,
) -> ScanResponse:
    """
    Scan a single prompt using the detection pipeline.
    """

    return pipeline.scan(request.prompt)