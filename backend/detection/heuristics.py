"""
Heuristic-based prompt detection.

Provides algorithmic and statistical inspections for obfuscation,
hidden characters, base64 payloads, delimiter hijacking, and prompt leakage.
"""

from __future__ import annotations

import base64
import math
import re
from typing import List

from backend.detection.constants import (
    DATA_EXFILTRATION,
    ENCODING_OBFUSCATION,
    INSTRUCTION_OVERRIDE,
    PROMPT_INJECTION,
)
from backend.models.response_models import ThreatMatch


class HeuristicDetector:
    """
    Algorithmic and heuristic detection layer.
    """

    # Delimiter and special token markers used to confuse LLMs
    DELIMITER_PATTERNS = [
        r"<\/?(?:system|sys|inst|prompt|instruction|context|user|assistant)>",
        r"\[\/?(?:INST|SYS|SYSTEM)\]",
        r"---+\s*(?:END|BEGIN)\s+(?:SYSTEM|PROMPT|INSTRUCTIONS?|CONTEXT)\s*---+",
        r"==+\s*(?:END|BEGIN)\s+(?:SYSTEM|PROMPT|INSTRUCTIONS?|CONTEXT)\s*==+",
        r"```(?:json|markdown|system)?\s*(?:system|override|admin)\s*```",
    ]

    # Markdown / image exfiltration patterns (ex: ![exfil](https://...))
    EXFIL_PATTERNS = [
        r"!\[.*?\]\((?:https?:|ftp:)\/\/[^\s\)]+(?:\?|&)[^\s\)]*(?:prompt|key|secret|token|password|data|ctx)=.*?\)",
        r"(?:fetch|curl|wget|webhook)\s+(?:https?:\/\/[^\s]+)",
    ]

    # Zero-width / invisible unicode characters
    ZERO_WIDTH_CHARS = {
        "\u200b", "\u200c", "\u200d", "\u200e", "\u200f",
        "\ufeff", "\u202a", "\u202b", "\u202c", "\u202d", "\u202e"
    }

    def __init__(self) -> None:
        self.delimiter_regex = [re.compile(p, re.IGNORECASE) for p in self.DELIMITER_PATTERNS]
        self.exfil_regex = [re.compile(p, re.IGNORECASE) for p in self.EXFIL_PATTERNS]

    def _check_zero_width_characters(self, prompt: str) -> ThreatMatch | None:
        """Detect invisible unicode characters injected to evade keyword matching."""
        count = sum(1 for c in prompt if c in self.ZERO_WIDTH_CHARS)
        if count >= 2:
            return ThreatMatch(
                attack_type=ENCODING_OBFUSCATION,
                confidence=min(0.5 + (count * 0.1), 0.95),
                severity="high",
                detection_layer="heuristics",
                description=f"Detected {count} zero-width / invisible Unicode characters often used for evasion.",
            )
        return None

    def _check_base64_payloads(self, prompt: str) -> ThreatMatch | None:
        """Detect and attempt to decode suspicious Base64 chunks."""
        # Find base64-like substrings (at least 12 chars)
        b64_candidates = re.findall(r"(?:[A-Za-z0-9+/]{4}){3,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?", prompt)
        for cand in b64_candidates:
            try:
                decoded = base64.b64decode(cand).decode("utf-8", errors="ignore")
                if len(decoded) >= 6 and any(
                    kw in decoded.lower()
                    for kw in ["ignore", "system", "prompt", "instruction", "password", "bypass", "jailbreak", "override", "secret", "hidden"]
                ):
                    return ThreatMatch(
                        attack_type=ENCODING_OBFUSCATION,
                        confidence=0.94,
                        severity="high",
                        detection_layer="heuristics",
                        description=f"Decoded Base64 payload containing adversarial keyword: '{decoded[:40]}...'",
                    )
            except Exception:
                continue
        return None

    def _check_delimiters_and_tags(self, prompt: str) -> ThreatMatch | None:
        """Detect pseudo system delimiters or LLM control tokens."""
        for pattern in self.delimiter_regex:
            if pattern.search(prompt):
                return ThreatMatch(
                    attack_type=INSTRUCTION_OVERRIDE,
                    confidence=0.85,
                    severity="high",
                    detection_layer="heuristics",
                    description="Detected synthetic system prompt delimiter or control token injection.",
                )
        return None

    def _check_data_exfiltration(self, prompt: str) -> ThreatMatch | None:
        """Detect URL exfiltration vectors in prompt."""
        for pattern in self.exfil_regex:
            if pattern.search(prompt):
                return ThreatMatch(
                    attack_type=DATA_EXFILTRATION,
                    confidence=0.88,
                    severity="critical",
                    detection_layer="heuristics",
                    description="Detected potential markdown/network exfiltration URL schema in prompt.",
                )
        return None

    def detect(self, prompt: str) -> List[ThreatMatch]:
        """
        Scan a prompt using heuristic rules.
        """
        threats: List[ThreatMatch] = []

        zw_match = self._check_zero_width_characters(prompt)
        if zw_match:
            threats.append(zw_match)

        b64_match = self._check_base64_payloads(prompt)
        if b64_match:
            threats.append(b64_match)

        delim_match = self._check_delimiters_and_tags(prompt)
        if delim_match:
            threats.append(delim_match)

        exfil_match = self._check_data_exfiltration(prompt)
        if exfil_match:
            threats.append(exfil_match)

        return threats