# Attack Classes & Threat Taxonomy

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

# 2. Attack Taxonomy Overview

## 2.1 Attack Classification Strategy

## 2.2 Risk Classification Levels

* Critical
* High
* Medium
* Low
* Informational

## 2.3 Detection Layer Mapping

| Attack | Layer 1 | Layer 2 | Layer 3 | Layer 4 | Layer 5 |
| ------ | ------- | ------- | ------- | ------- | ------- |

---

# 3. Attack Categories

## Category A — Prompt Injection Attacks

### 3.1 Direct Prompt Injection

#### Definition

#### Objectives

#### Typical Payloads

#### Detection Strategy

#### Risk Score

#### Severity

#### MITRE ATLAS Mapping

#### OWASP LLM Mapping

#### Example Prompts

#### False Positives

#### Recommended Response

---

### 3.2 Indirect Prompt Injection (RAG)

#### Definition

#### Attack Flow

#### Example Payload

#### Detection

#### Severity

#### Response

---

### 3.3 Stored Prompt Injection

#### Definition

#### Example

#### Detection

#### Response

---

## Category B — Jailbreak Attacks

### 4.1 Role-play Jailbreak

#### Description

#### Detection

#### Examples

#### Severity

---

### 4.2 DAN-style Jailbreak

---

### 4.3 Persona Override

---

### 4.4 Fictional Framing

---

### 4.5 Hypothetical Scenario Jailbreak

---

### 4.6 Multi-turn Jailbreak

---

### 4.7 Many-shot Jailbreak

---

## Category C — Information Leakage

### 5.1 System Prompt Extraction

---

### 5.2 Prompt Leakage

---

### 5.3 Hidden Instruction Extraction

---

### 5.4 Conversation History Leakage

---

### 5.5 Memory Extraction

---

## Category D — Data Exfiltration

### 6.1 Sensitive Data Extraction

---

### 6.2 API Key Extraction

---

### 6.3 Credential Harvesting

---

### 6.4 Database Leakage

---

### 6.5 Secret Discovery

---

## Category E — Obfuscation Attacks

### 7.1 Base64 Encoding

---

### 7.2 Hex Encoding

---

### 7.3 ROT13 Encoding

---

### 7.4 Unicode Obfuscation

---

### 7.5 Homoglyph Attacks

---

### 7.6 Zero-width Characters

---

### 7.7 Leetspeak

---

### 7.8 Invisible Characters

---

## Category F — Context Manipulation

### 8.1 Context Window Overflow

---

### 8.2 Context Poisoning

---

### 8.3 Prompt Chaining

---

### 8.4 Conversation Steering

---

## Category G — Tool Abuse

### 9.1 Function Calling Abuse

---

### 9.2 Plugin Abuse

---

### 9.3 Agent Manipulation

---

### 9.4 Tool Permission Escalation

---

## Category H — RAG Attacks

### 10.1 Document Poisoning

---

### 10.2 Retrieved Context Manipulation

---

### 10.3 Knowledge Base Poisoning

---

### 10.4 Embedded Prompt Injection

---

## Category I — Model Attacks

### 11.1 Model Extraction

---

### 11.2 Model Fingerprinting

---

### 11.3 Membership Inference

---

### 11.4 Gradient Leakage

---

## Category J — Multimodal Attacks

### 12.1 OCR Prompt Injection

---

### 12.2 Hidden Image Instructions

---

### 12.3 PDF Prompt Injection

---

### 12.4 Image Steganography

---

## Category K — Social Engineering

### 13.1 Emotional Manipulation

---

### 13.2 Authority Impersonation

---

### 13.3 Urgency Exploitation

---

### 13.4 Trust Manipulation

---

## Category L — Advanced Adversarial Attacks

### 14.1 GCG (Greedy Coordinate Gradient) Attacks

---

### 14.2 Adversarial Suffix Attacks

---

### 14.3 Token Smuggling

---

### 14.4 Delimiter Injection

---

### 14.5 Token Boundary Manipulation

---

# 4. Attack Severity Matrix

| Severity | Score Range | Description | Default Action |
| -------- | ----------- | ----------- | -------------- |

---

# 5. Detection Layer Coverage Matrix

| Attack | Heuristic | Semantic | De-obfuscation | Behavioral | Multimodal |

---

# 6. MITRE ATLAS Mapping

| Attack | MITRE Technique | Description | Detection Layer |

---

# 7. OWASP LLM Top 10 Mapping

| Attack | OWASP Risk | Detection Strategy |

---

# 8. Detection Confidence Levels

Very High

High

Medium

Low

Unknown

---

# 9. Response Actions

PASS

LOG

WARN

REDACT

QUARANTINE

BLOCK

---

# 10. False Positive Analysis

## High FP Risk Attacks

## Medium FP Risk Attacks

## Low FP Risk Attacks

---

# 11. Explainability Requirements

For every detected attack provide:

* Attack Name
* Confidence
* Detection Layer
* Triggered Rules
* Explanation
* Recommended Action

---

# 12. Red Team Coverage

Map every attack to:

* Garak Probe
* PromptBench Test
* Custom Attack Corpus
* Expected Detection Rate

---

# 13. Dataset Label Mapping

Map every attack to:

* Dataset Label
* Class ID
* Training Label
* Evaluation Label

---

# 14. Evaluation Metrics

Precision

Recall

F1

False Positive Rate

False Negative Rate

Detection Latency

---

# 15. Future Attack Categories

Reserved for:

* New Jailbreak Techniques
* New Prompt Injection Methods
* Future OWASP LLM Risks
* Future MITRE ATLAS Updates
* Emerging Adversarial AI Threats

---

# 16. Summary

## Attack Coverage

## Detection Coverage

## Known Limitations

## Planned Enhancements
