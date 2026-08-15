"""
Regex-based adversarial prompt detector.

This detector scans incoming prompts using curated regular
expressions and produces structured ThreatMatch objects.
"""

from __future__ import annotations

import re
from typing import Dict, List, Literal, Pattern, TypeAlias

from backend.detection.constants import (
    REGEX_PATTERNS,
    RISK_WEIGHTS,
)
from backend.models.response_models import ThreatMatch


# ============================================================
# Type Aliases
# ============================================================

Severity: TypeAlias = Literal[
    "low",
    "medium",
    "high",
    "critical",
]


# ============================================================
# RegexDetector
# ============================================================

class RegexDetector:
    """
    Detect adversarial prompts using compiled regular expressions.
    """

    def __init__(self) -> None:
        """
        Compile all regex patterns once during startup.
        """

        self.patterns: Dict[str, List[Pattern[str]]] = {
            attack_type: [
                re.compile(pattern, re.IGNORECASE)
                for pattern in patterns
            ]
            for attack_type, patterns in REGEX_PATTERNS.items()
        }

    def detect(self, prompt: str) -> list[ThreatMatch]:
        """
        Scan a prompt for regex-based adversarial attacks.

        Parameters
        ----------
        prompt : str
            User supplied prompt.

        Returns
        -------
        list[ThreatMatch]
            Detected threats.
        """

        threats: list[ThreatMatch] = []

        normalized_prompt = prompt.strip()

        for attack_type, patterns in self.patterns.items():

            matched_patterns = sum(
                1
                for pattern in patterns
                if pattern.search(normalized_prompt)
            )

            if matched_patterns == 0:
                continue

            confidence = round(
                min(0.75 + (0.12 * (matched_patterns - 1)), 0.99),
                2,
            )

            weight = RISK_WEIGHTS.get(attack_type, 10)

            severity: Severity

            if weight >= 35:
                severity = "critical"
            elif weight >= 30:
                severity = "high"
            elif weight >= 20:
                severity = "medium"
            else:
                severity = "low"

            threats.append(
                ThreatMatch(
                    attack_type=attack_type,
                    confidence=round(confidence, 2),
                    severity=severity,
                    detection_layer="regex",
                    description=(
                        "Regex detector identified "
                        f"{matched_patterns} matching signature(s)."
                    ),
                )
            )

        return threats