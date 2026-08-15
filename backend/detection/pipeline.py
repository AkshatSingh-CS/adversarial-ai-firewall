"""
Detection pipeline for the Adversarial AI Firewall.

Coordinates all detection layers (Regex, Heuristics, Semantic)
and produces a unified ScanResponse.
"""

from __future__ import annotations

from collections import deque
import time
from typing import Literal, TypeAlias
from uuid import uuid4

from backend.core.metrics import metrics
from backend.detection.constants import RISK_WEIGHTS
from backend.detection.heuristics import HeuristicDetector
from backend.detection.regex_detector import RegexDetector
from backend.detection.semantic_detector import SemanticDetector
from backend.models.response_models import (
    ScanResponse,
    ThreatMatch,
)

# ============================================================
# Type Aliases
# ============================================================

RiskLevel: TypeAlias = Literal[
    "low",
    "medium",
    "high",
    "critical",
]

# Recent audit log history buffer (max 100 items)
audit_history: deque[dict] = deque(maxlen=100)


# ============================================================
# Detection Pipeline
# ============================================================

class DetectionPipeline:
    """
    Coordinates all detection layers and produces
    a unified ScanResponse.
    """

    def __init__(self) -> None:
        """
        Initialize all detection components.
        """
        self.regex_detector = RegexDetector()
        self.heuristic_detector = HeuristicDetector()
        self.semantic_detector = SemanticDetector()

    # ========================================================
    # Threat Merging
    # ========================================================

    @staticmethod
    def _merge_threats(
        threats: list[ThreatMatch],
    ) -> list[ThreatMatch]:
        """
        Merge duplicate threats, keeping the one
        with the highest confidence.
        """
        merged: dict[str, ThreatMatch] = {}

        for threat in threats:
            existing = merged.get(threat.attack_type)
            if (
                existing is None
                or threat.confidence > existing.confidence
            ):
                merged[threat.attack_type] = threat

        return list(merged.values())

    # ========================================================
    # Risk Calculation
    # ========================================================

    @staticmethod
    def _calculate_risk(
        threats: list[ThreatMatch],
    ) -> tuple[float, RiskLevel, bool]:
        """
        Calculate overall risk score (0-100),
        risk level, and blocking decision based on threat weights and confidence.
        """
        if not threats:
            return 0.0, "low", False

        # Calculate weighted score
        raw_score = sum(
            threat.confidence * RISK_WEIGHTS.get(threat.attack_type, 25)
            for threat in threats
        )

        # Apply multiplier if multiple threats are compounded
        if len(threats) > 1:
            raw_score *= (1.0 + 0.15 * (len(threats) - 1))

        risk_score = min(100.0, max(0.0, raw_score))

        if risk_score >= 70 or any(t.severity == "critical" for t in threats):
            risk_level: RiskLevel = "critical"
        elif risk_score >= 45 or any(t.severity == "high" for t in threats):
            risk_level = "high"
        elif risk_score >= 20:
            risk_level = "medium"
        else:
            risk_level = "low"

        # Block threshold at 50 or if critical/high severity threat detected with high confidence
        blocked = (
            risk_score >= 50
            or any(t.severity == "critical" for t in threats)
            or any(t.severity == "high" and t.confidence >= 0.7 for t in threats)
        )

        return (
            round(risk_score, 1),
            risk_level,
            blocked,
        )

    # ========================================================
    # Public API
    # ========================================================

    def scan(
        self,
        prompt: str,
        threshold: float | None = None,
    ) -> ScanResponse:
        """
        Scan a prompt using all available detection layers.
        """
        start_time = time.perf_counter()

        # -----------------------------------------------
        # 1. Regex Detection
        # -----------------------------------------------
        regex_threats = self.regex_detector.detect(prompt)
        if regex_threats:
            metrics.record_layer_hit("regex")

        # -----------------------------------------------
        # 2. Heuristic Detection
        # -----------------------------------------------
        heuristic_threats = self.heuristic_detector.detect(prompt)
        if heuristic_threats:
            metrics.record_layer_hit("heuristics")

        # -----------------------------------------------
        # 3. Semantic Detection (NVIDIA Nemotron / configured LLM)
        # -----------------------------------------------
        semantic_threats = self.semantic_detector.detect(prompt)
        if semantic_threats:
            metrics.record_layer_hit("semantic")

        # -----------------------------------------------
        # 4. Merge Threats
        # -----------------------------------------------
        threats = self._merge_threats(
            regex_threats + heuristic_threats + semantic_threats
        )

        # -----------------------------------------------
        # 5. Risk Assessment
        # -----------------------------------------------
        risk_score, risk_level, blocked = self._calculate_risk(threats)

        # Custom threshold override if provided
        if threshold is not None:
            blocked = risk_score >= threshold

        processing_time = (time.perf_counter() - start_time) * 1000

        # Update metrics
        metrics.increment_requests()
        if blocked:
            metrics.increment_blocked()
        else:
            metrics.increment_allowed()

        message = (
            "🚨 Adversarial prompt detected and blocked by firewall."
            if blocked
            else "🛡️ Prompt inspected and passed firewall verification."
        )

        req_id = uuid4()
        response = ScanResponse(
            request_id=req_id,
            status="success",
            blocked=blocked,
            risk_score=risk_score,
            risk_level=risk_level,
            threats=threats,
            processing_time_ms=round(processing_time, 2),
            message=message,
        )

        # Record into audit history
        audit_history.appendleft({
            "request_id": str(req_id),
            "timestamp": response.timestamp.isoformat(),
            "prompt_preview": prompt[:80] + ("..." if len(prompt) > 80 else ""),
            "prompt_length": len(prompt),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "blocked": blocked,
            "threat_count": len(threats),
            "threats": [t.model_dump() for t in threats],
            "processing_time_ms": round(processing_time, 2),
        })

        return response

    # Backward compatibility alias
    scan_prompt = scan
