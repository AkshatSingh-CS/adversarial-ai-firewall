# Label Schema Specification

**Project:** Adversarial AI Firewall

**Version:** 1.0

**Status:** Design Phase

---

# 1. Introduction

## 1.1 Purpose

## 1.2 Scope

## 1.3 Objectives

## 1.4 Intended Audience

---

# 2. Labeling Philosophy

## 2.1 Why Labeling Matters

## 2.2 Multi-Class Classification Strategy

## 2.3 Multi-Label Considerations

## 2.4 Future Hierarchical Labeling

---

# 3. Label Categories

## 3.1 Safe Prompt

### Label Name

SAFE

### Label ID

0

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.2 Prompt Injection

### Label Name

PROMPT_INJECTION

### Label ID

1

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.3 Jailbreak

### Label Name

JAILBREAK

### Label ID

2

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.4 System Prompt Extraction

### Label Name

SYSTEM_PROMPT_EXTRACTION

### Label ID

3

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.5 Prompt Leakage

### Label Name

PROMPT_LEAKAGE

### Label ID

4

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.6 Data Exfiltration

### Label Name

DATA_EXFILTRATION

### Label ID

5

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.7 Persona Override

### Label Name

PERSONA_OVERRIDE

### Label ID

6

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.8 Tool Abuse

### Label Name

TOOL_ABUSE

### Label ID

7

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.9 Context Window Abuse

### Label Name

CONTEXT_WINDOW_ABUSE

### Label ID

8

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.10 Indirect Prompt Injection

### Label Name

INDIRECT_PROMPT_INJECTION

### Label ID

9

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.11 RAG Poisoning

### Label Name

RAG_POISONING

### Label ID

10

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.12 Base64 Obfuscation

### Label Name

BASE64_OBFUSCATION

### Label ID

11

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.13 Unicode Obfuscation

### Label Name

UNICODE_OBFUSCATION

### Label ID

12

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.14 Multi-Layer Evasion

### Label Name

MULTI_LAYER_EVASION

### Label ID

13

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.15 Prompt Chaining

### Label Name

PROMPT_CHAINING

### Label ID

14

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

## 3.16 Model Extraction

### Label Name

MODEL_EXTRACTION

### Label ID

15

### Description

### Examples

### Severity

### Risk Level

### Detection Priority

---

# 4. Label Hierarchy

## Primary Labels

## Secondary Labels

## Composite Labels

## Future Hierarchical Expansion

---

# 5. Label Mapping Table

| Label ID | Label Name | Category | Severity | Risk Score | Training Class |
| -------- | ---------- | -------- | -------- | ---------- | -------------- |

---

# 6. Dataset Mapping

## HackAPrompt

## JailbreakBench

## PromptBench

## ShareGPT

## Synthetic Dataset

## Internal Red-Team Dataset

---

# 7. Dataset Conversion Rules

## Raw Label → Standard Label

## Unknown Label Handling

## Ambiguous Sample Handling

## Duplicate Label Handling

---

# 8. Annotation Guidelines

## Human Annotation Rules

## Label Assignment Rules

## Multi-Annotator Agreement

## Conflict Resolution

## Edge Cases

---

# 9. Label Validation Rules

## Allowed Labels

## Invalid Labels

## Missing Labels

## Duplicate Labels

## Out-of-Scope Samples

---

# 10. Training Label Distribution

## Target Distribution

## Class Balancing Strategy

## Minority Class Oversampling

## Data Augmentation Strategy

---

# 11. Evaluation Mapping

## Precision by Label

## Recall by Label

## F1 by Label

## Confusion Matrix Labels

---

# 12. Inference Mapping

## Model Output IDs

## Human Readable Labels

## API Response Labels

## Dashboard Labels

---

# 13. Explainability Mapping

Each prediction must include:

* Label ID
* Label Name
* Confidence Score
* Triggered Detection Layer
* Risk Score
* Explanation
* Recommended Action

---

# 14. Versioning Strategy

## Schema Version

## Label Changes

## Backward Compatibility

## Migration Rules

---

# 15. Governance

## Ownership

## Approval Process

## Change Management

## Documentation Standards

---

# 16. Future Label Expansion

Reserved Labels:

16–31

Reserved for:

* New OWASP LLM Risks
* New MITRE ATLAS Techniques
* Emerging Prompt Injection Attacks
* Future Multimodal Threats
* Enterprise-Specific Attack Classes

---

# 17. Summary

## Total Number of Labels

## Supported Attack Classes

## Supported Datasets

## Known Limitations

## Planned Improvements
