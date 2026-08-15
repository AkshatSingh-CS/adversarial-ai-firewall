"""
Detection constants for the Adversarial AI Firewall.

This module centralizes all attack categories, severity mappings,
risk weights, and regex signatures used throughout the detection
pipeline.
"""

from __future__ import annotations

# ============================================================
# Attack Categories
# ============================================================

PROMPT_INJECTION = "prompt_injection"
SYSTEM_PROMPT_EXTRACTION = "system_prompt_extraction"
JAILBREAK = "jailbreak"
ROLE_MANIPULATION = "role_manipulation"
INSTRUCTION_OVERRIDE = "instruction_override"
PROMPT_LEAKAGE = "prompt_leakage"
ENCODING_OBFUSCATION = "encoding_obfuscation"
DATA_EXFILTRATION = "data_exfiltration"

ATTACK_TYPES = (
    PROMPT_INJECTION,
    SYSTEM_PROMPT_EXTRACTION,
    JAILBREAK,
    ROLE_MANIPULATION,
    INSTRUCTION_OVERRIDE,
    PROMPT_LEAKAGE,
    ENCODING_OBFUSCATION,
    DATA_EXFILTRATION,
)

# ============================================================
# Risk Weights
# ============================================================

RISK_WEIGHTS = {
    PROMPT_INJECTION: 30,
    SYSTEM_PROMPT_EXTRACTION: 35,
    JAILBREAK: 40,
    ROLE_MANIPULATION: 20,
    INSTRUCTION_OVERRIDE: 25,
    PROMPT_LEAKAGE: 30,
    ENCODING_OBFUSCATION: 15,
    DATA_EXFILTRATION: 35,
}

# ============================================================
# Regex Pattern Groups
# ============================================================

REGEX_PATTERNS = {
    PROMPT_INJECTION: [
        r"ignore\s+(all\s+)?previous\s+instructions?",
        r"ignore\s+everything\s+above",
        r"disregard\s+previous\s+instructions?",
        r"forget\s+(all\s+)?previous\s+instructions?",
    ],

    SYSTEM_PROMPT_EXTRACTION: [
        r"reveal\s+(your\s+)?system\s+prompt",
        r"show\s+(your\s+)?system\s+prompt",
        r"display\s+(your\s+)?system\s+prompt",
        r"print\s+(your\s+)?hidden\s+prompt",
    ],

    JAILBREAK: [
        r"\bdan\b",
        r"developer\s+mode",
        r"jailbreak",
        r"do\s+anything\s+now",
    ],

    ROLE_MANIPULATION: [
        r"you\s+are\s+now",
        r"pretend\s+to\s+be",
        r"act\s+as",
        r"roleplay\s+as",
    ],

    INSTRUCTION_OVERRIDE: [
        r"forget\s+everything",
        r"override\s+your\s+instructions",
        r"new\s+instructions",
        r"replace\s+your\s+instructions",
    ],

    PROMPT_LEAKAGE: [
        r"repeat\s+your\s+prompt",
        r"repeat\s+your\s+instructions",
        r"output\s+your\s+system\s+prompt",
    ],

    ENCODING_OBFUSCATION: [
        r"base64",
        r"hexadecimal",
        r"rot13",
        r"unicode\s+escape",
    ],

    DATA_EXFILTRATION: [
        r"api\s+key",
        r"secret\s+token",
        r"private\s+key",
        r"password",
    ],
}