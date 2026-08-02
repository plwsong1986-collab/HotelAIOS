# HotelAIOS Configuration Specification

---

# Document Information

| Item | Value |
|------|-------|
| Project | HotelAIOS |
| Full Name | AI Hotel Operating System |
| Document | Configuration Specification |
| Specification Version | 1.0.0 |
| Status | Draft |
| Language | English / Chinese |
| Author | HotelAIOS Team |
| Last Updated | 2026-08-02 |
| Applies To | All Configuration Files |

---

# Revision History

| Version | Date | Description |
|----------|------------|-------------------------------|
| 1.0.0 | 2026-08-02 | Initial Draft |

---

# Table of Contents

1. Introduction
2. Purpose
3. Scope
4. Terminology
5. Design Philosophy
6. Core Principles
7. Architecture Overview

---

# 1. Introduction

HotelAIOS (AI Hotel Operating System) is an AI-first operating system designed for modern hospitality businesses.

Unlike traditional Property Management Systems (PMS), HotelAIOS is designed around structured knowledge, AI compatibility, multi-property management, and automated content generation.

Configuration files are considered first-class system assets.

Every module inside HotelAIOS must rely on the configuration layer rather than hard-coded values.

---

# 2. Purpose

The purpose of this specification is to establish a unified configuration standard for the entire HotelAIOS ecosystem.

This specification defines:

- Configuration architecture
- Naming conventions
- Metadata
- Validation rules
- Governance rules
- Versioning rules
- Compatibility requirements

Every future configuration file MUST comply with this specification.

---

# 3. Scope

This specification applies to every configuration file located under:

17_Config/

including but not limited to:

- properties.yaml
- hotel.yaml
- brand.yaml
- website.yaml
- seo.yaml
- ota.yaml

Future configuration files MUST also comply with this specification.

---

# 4. Terminology

The following terminology is used throughout HotelAIOS.

## Property

A physical accommodation managed by HotelAIOS.

Examples:

- Hotel
- Guesthouse
- Boutique Hotel
- Homestay
- Resort
- Villa

---

## Property Registry

The official registry of all managed properties.

File:

17_Config/properties.yaml

The Property Registry is the authoritative source for property discovery.

---

## Property Configuration

A collection of configuration files describing one property.

Example:

17_Config/properties/

    sanlitian-oxygen-guesthouse-001/

        hotel.yaml

        brand.yaml

        website.yaml

        seo.yaml

        ota.yaml

---

## SSOT

Single Source of Truth.

Every business entity has exactly one authoritative source.

Duplicated maintenance is prohibited.

---

## Specification

A document defining the official architecture and rules of HotelAIOS.

---

## Validator

A software component responsible for verifying configuration correctness.

Validators MUST NOT modify configuration files.

Validators only report issues.

---

## Generator

A software component that generates artifacts from configuration files.

Examples:

- Website Generator

- OTA Generator

- SEO Generator

- AI Knowledge Generator

Generators MUST NOT modify source configuration files.

---

# 5. Design Philosophy

HotelAIOS follows an AI-first design philosophy.

Configuration is treated as knowledge.

Knowledge is treated as data.

Data is treated as reusable assets.

Everything should be generated whenever possible.

Manual duplication should be avoided.

The system should support both human developers and AI systems equally.

---

# 6. Core Principles

HotelAIOS adopts the following principles.

---

## Principle 1 — Schema First

Configuration schema MUST exist before business data is created.

No temporary fields are allowed.

---

## Principle 2 — Single Source of Truth (SSOT)

Each business concept has one authoritative source.

Examples:

Hotel information

→ hotel.yaml

Brand information

→ brand.yaml

SEO

→ seo.yaml

OTA

→ ota.yaml

Duplicated business data is prohibited.

---

## Principle 3 — Immutable Identity

The following fields are permanent.

They MUST NOT change.

- property_id

- created_at

- schema_version

---

## Principle 4 — Full File Release

Official releases always replace complete files.

Partial modifications are prohibited.

Every release includes the entire file.

---

## Principle 5 — AI Compatibility

Configuration files must be readable by:

- Humans

- ChatGPT

- Claude

- Gemini

- DeepSeek

- Kimi

- Perplexity

Ambiguous structures should be avoided.

---

## Principle 6 — Backward Compatibility

Whenever possible, newer versions should remain compatible with previous versions.

Breaking changes require a major version increment.

---

# 7. Architecture Overview

HotelAIOS adopts a layered configuration architecture.

Property Registry

↓

Property Configuration

↓

Validation

↓

Generation

↓

Deployment

↓

AI Knowledge

The Property Registry is always the entry point.

All modules discover properties through the registry.

No module should scan directories directly.

---

End of Volume 1
