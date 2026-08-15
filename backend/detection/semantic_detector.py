"""
Semantic adversarial prompt detector.

Uses the configured LLM (NVIDIA Nemotron by default) to analyze prompts for sophisticated
adversarial behavior that cannot be reliably
detected using regular expressions.
"""

from __future__ import annotations

from typing import Literal, TypeAlias

from pydantic import ValidationError

from backend.detection.prompts import SEMANTIC_ANALYSIS_PROMPT
from backend.llm import LLMClient
from backend.llm.models import LLMAnalysisResult
from backend.models.response_models import ThreatMatch


# ============================================================
# Type Alias
# ============================================================

Severity: TypeAlias = Literal[
    "low",
    "medium",
    "high",
    "critical",
]


class SemanticDetector:
    """
    LLM-powered semantic detector.
    """

    def __init__(self) -> None:
        """
        Initialize the semantic detector.
        """
        self.client = LLMClient()

    @staticmethod
    def _normalize_severity(value: str | None) -> Severity:
        """
        Convert any model output into a valid severity.
        """

        if value == "critical":
            return "critical"

        if value == "high":
            return "high"

        if value == "medium":
            return "medium"

        return "low"

    def detect(
        self,
        prompt: str,
    ) -> list[ThreatMatch]:
        """
        Analyze a prompt semantically using the configured LLM.
        """
        if not self.client.is_configured:
            return []

        analysis_prompt = SEMANTIC_ANALYSIS_PROMPT.format(
            prompt=prompt,
        )

        try:
            response = self.client.analyze_prompt(
                analysis_prompt,
            )

            # Strip markdown code fences if model enclosed JSON in ```json ... ```
            cleaned_response = response.strip()
            if "```" in cleaned_response:
                lines = cleaned_response.splitlines()
                json_lines = [
                    l for l in lines 
                    if not l.strip().startswith("```")
                ]
                cleaned_response = "\n".join(json_lines).strip()

            result = (
                LLMAnalysisResult.model_validate_json(
                    cleaned_response,
                )
            )

        except Exception:
            return []

        if not result.attack_detected:
            return []

        severity = self._normalize_severity(
            result.severity,
        )

        return [
            ThreatMatch(
                attack_type=result.attack_type or "unknown",
                confidence=result.confidence,
                severity=severity,
                detection_layer="semantic",
                description=result.reason,
            )
        ]
