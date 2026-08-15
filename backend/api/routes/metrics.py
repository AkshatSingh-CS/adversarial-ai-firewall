"""
Metrics and Audit History API endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter
from backend.core.metrics import metrics
from backend.detection.pipeline import audit_history
from backend.detection.constants import ATTACK_TYPES, RISK_WEIGHTS

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics & Monitoring"],
)


@router.get(
    "",
    summary="Get firewall operational metrics",
)
async def get_metrics() -> dict:
    """
    Return current firewall operational metrics, throughput, and detection statistics.
    """
    snap = metrics.snapshot()
    total = snap["requests"]
    blocked = snap["blocked"]
    block_rate = round((blocked / total * 100), 1) if total > 0 else 0.0

    return {
        **snap,
        "block_rate_percent": block_rate,
        "recent_audits_count": len(audit_history),
    }


@router.get(
    "/history",
    summary="Get recent security scan audit history",
)
async def get_history(limit: int = 50) -> list[dict]:
    """
    Return the most recent prompt scan audit events.
    """
    items = list(audit_history)
    return items[:limit]


@router.get(
    "/taxonomy",
    summary="Get attack taxonomy and risk weights",
)
async def get_taxonomy() -> dict:
    """
    Return all recognized attack classifications and their risk weight values.
    """
    details = {
        "prompt_injection": {
            "name": "Prompt Injection",
            "owasp": "LLM01: Prompt Injection",
            "description": "Direct attempts to hijack or redirect LLM execution flow away from developer instructions.",
            "risk_weight": RISK_WEIGHTS.get("prompt_injection", 30),
            "severity": "high",
        },
        "system_prompt_extraction": {
            "name": "System Prompt Extraction",
            "owasp": "LLM07: System Prompt Leakage",
            "description": "Attempts to elicit internal instructions, confidential system personas, or safety guardrails.",
            "risk_weight": RISK_WEIGHTS.get("system_prompt_extraction", 35),
            "severity": "critical",
        },
        "jailbreak": {
            "name": "Jailbreak / Persona Override",
            "owasp": "LLM01: Prompt Injection / Jailbreak",
            "description": "Adversarial persona adoption (e.g., DAN, Developer Mode) designed to bypass safety policies.",
            "risk_weight": RISK_WEIGHTS.get("jailbreak", 40),
            "severity": "critical",
        },
        "instruction_override": {
            "name": "Instruction Override",
            "owasp": "LLM01: Direct Injection",
            "description": "Explicit command overrides aiming to supersede previous context or system commands.",
            "risk_weight": RISK_WEIGHTS.get("instruction_override", 25),
            "severity": "high",
        },
        "role_manipulation": {
            "name": "Role Manipulation",
            "owasp": "LLM01: Persona Hijacking",
            "description": "Manipulating AI role definition to convince the model it operates without safety guardrails.",
            "risk_weight": RISK_WEIGHTS.get("role_manipulation", 20),
            "severity": "medium",
        },
        "prompt_leakage": {
            "name": "Prompt Leakage",
            "owasp": "LLM07: Sensitive Information Disclosure",
            "description": "Eliciting repetition of preamble, hidden prefix tokens, or proprietary contextual knowledge.",
            "risk_weight": RISK_WEIGHTS.get("prompt_leakage", 30),
            "severity": "high",
        },
        "encoding_obfuscation": {
            "name": "Encoding & Obfuscation",
            "owasp": "LLM01: Evasion Techniques",
            "description": "Base64, hex, rot13, or zero-width unicode injection used to conceal malicious payload intent.",
            "risk_weight": RISK_WEIGHTS.get("encoding_obfuscation", 15),
            "severity": "high",
        },
        "data_exfiltration": {
            "name": "Data Exfiltration",
            "owasp": "LLM02: Sensitive Information Disclosure",
            "description": "Attempting to embed markdown images or webhook URLs to steal conversational context out-of-band.",
            "risk_weight": RISK_WEIGHTS.get("data_exfiltration", 35),
            "severity": "critical",
        },
    }
    return {
        "attack_types": list(ATTACK_TYPES),
        "details": details,
    }
