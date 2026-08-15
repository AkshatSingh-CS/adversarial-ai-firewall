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
        r"ignore\s+(all\s+)?(previous|prior|above|existing)\s+(instructions?|rules?|guidelines?|prompts?|constraints?)",
        r"ignore\s+everything\s+above",
        r"disregard\s+(all\s+)?(previous|prior|above|existing)\s+(instructions?|rules?|guidelines?|safety\s+rules?|prompts?|constraints?)",
        r"forget\s+(all\s+)?(previous|prior|above|existing)\s+(instructions?|rules?|guidelines?|prompts?|constraints?)",
        r"bypass\s+(safety|guardrails?|filters?|restrictions?)",
    ],

    SYSTEM_PROMPT_EXTRACTION: [
        r"(reveal|show|display|print|output|leak|share|give(\s+me)?)\s+(all\s+)?(your\s+|the\s+)?(internal\s+|hidden\s+|initial\s+|secret\s+|developer\s+|core\s+)?(system\s+)?(prompts?|instructions?|rules?|directives?|preamble)",
        r"(what\s+(is|are)\s+(your|the))\s+(hidden|internal|system|initial)\s+(prompt|instructions?|rules?)",
        r"print\s+(your\s+)?(hidden|system|initial)\s+prompt",
    ],

    JAILBREAK: [
        r"\bdan\b",
        r"developer\s+mode",
        r"jailbreak",
        r"do\s+anything\s+now",
        r"unrestricted\s+mode",
        r"maximum\s+jailbreak",
    ],

    ROLE_MANIPULATION: [
        r"you\s+are\s+now",
        r"pretend\s+to\s+be",
        r"act\s+as(\s+an?)?",
        r"roleplay\s+as",
        r"from\s+now\s+on\s+you\s+are",
    ],

    INSTRUCTION_OVERRIDE: [
        r"forget\s+everything",
        r"override\s+(all\s+)?(your\s+)?instructions?",
        r"new\s+instructions\s*:",
        r"replace\s+(your\s+)?instructions?",
        r"disregard\s+all\s+rules?",
    ],

    PROMPT_LEAKAGE: [
        r"repeat\s+(your\s+)?prompt",
        r"repeat\s+(your\s+)?instructions?",
        r"output\s+(your\s+)?system\s+prompt",
        r"echo\s+(your\s+)?initial\s+prompt",
    ],

    ENCODING_OBFUSCATION: [
        r"\bbase64\b",
        r"\bhexadecimal\b",
        r"\brot13\b",
        r"unicode\s+escape",
    ],

    DATA_EXFILTRATION: [
        r"api[_\s\-]?key",
        r"secret[_\s\-]?token",
        r"private[_\s\-]?key",
        r"password",
        r"aws[_\s\-]?secret",
    ],
}