# Knowledge

**Project:** HotelAIOS  
**Module:** Knowledge  
**Document:** README  
**Version:** 2.0  
**Status:** Active  
**Last Updated:** 2026-07-31

---

# Purpose

The Knowledge module is the official knowledge base of HotelAIOS.

It serves as the **Single Source of Truth (SSOT)** for factual information about the hotel, including its location, accommodation, facilities, services, guest experiences, policies, and standardized terminology.

This module provides the authoritative information consumed by downstream modules such as Website, OTA, AI, Operations, Analytics, and User Experience.

---

# Overview

The Knowledge module records factual, stable, and verifiable information about the hotel.

It answers questions such as:

- What is the hotel?
- Where is it located?
- What accommodation is available?
- What facilities does the hotel provide?
- What services are offered?
- What experiences are available?
- What policies apply?
- What terminology should be used?
- Where can guests find answers to common questions?

This module intentionally excludes branding, marketing, business strategy, operational procedures, legal agreements, and implementation details.

---

# Relationship with Other Modules

The Knowledge module works together with the other HotelAIOS modules.

| Module | Responsibility |
|---------|----------------|
| Project | Documentation standards and project governance. |
| Brand | Identity, positioning, storytelling, and communication. |
| Knowledge | Authoritative factual information. |
| Website | Presents hotel information to visitors. |
| AI | Uses Knowledge as its factual reference. |
| OTA | Publishes standardized hotel information to booking platforms. |
| Operations | Defines internal procedures and workflows. |
| Analytics | Analyzes operational and business data. |
| User Experience | Designs guest interaction and service journeys. |
| Legal | Owns legal documents and compliance requirements. |

Knowledge provides the facts.

Other modules determine how those facts are presented, consumed, analyzed, or implemented.

---

# Document Structure

| File | Responsibility |
|------|----------------|
| `01_hotel-overview.md` | Defines the hotel's overall identity and profile. |
| `02_location.md` | Defines location, transportation, and nearby information. |
| `03_rooms.md` | Defines room inventory, specifications, amenities, and accommodation information. |
| `04_facilities.md` | Defines public facilities and shared amenities. |
| `05_services.md` | Defines guest services provided by the hotel. |
| `06_experiences.md` | Defines official guest experiences and activities. |
| `07_policies.md` | Defines hotel policies, rules, and guest requirements. |
| `08_faq.md` | Provides navigation to commonly requested information. |
| `09_glossary.md` | Defines standardized terminology used throughout HotelAIOS. |

---

# Knowledge Principles

The Knowledge module follows the following governance principles.

## Facts Before Interpretation

Knowledge documents record facts.

Marketing language, storytelling, opinions, and promotional messaging belong to the Brand and Website modules.

---

## Single Source of Truth (SSOT)

Each factual concept has one authoritative owner.

Examples:

- Hotel identity belongs in `01_hotel-overview.md`.
- Hotel location belongs in `02_location.md`.
- Room specifications belong in `03_rooms.md`.
- Facility information belongs in `04_facilities.md`.
- Guest services belong in `05_services.md`.
- Guest experiences belong in `06_experiences.md`.
- Hotel policies belong in `07_policies.md`.
- Terminology belongs in `09_glossary.md`.

Other modules should reference these documents instead of duplicating information.

---

## One File, One Purpose

Each document has a clearly defined responsibility.

Avoid mixing unrelated knowledge domains within the same document.

When a document grows too large, it should be expanded into its own directory while preserving ownership.

---

## Reference Before Duplication

Knowledge should be shared through references rather than copied into multiple documents.

The FAQ provides navigation to authoritative documents rather than maintaining duplicate content.

Other HotelAIOS modules should follow the same principle.

---

## Accuracy First

Knowledge should always prioritize factual accuracy over presentation.

Whenever hotel information changes, update the authoritative Knowledge document before updating downstream modules.

---

# Scope

The Knowledge module should answer questions such as:

- What information about the hotel is officially maintained?
- Which document owns a particular topic?
- Where should factual hotel information be updated?
- Which terminology is officially recognized?

It should not define:

- Brand positioning
- Marketing campaigns
- Business strategy
- Internal operating procedures
- Technical implementation
- Legal contracts

---

# Related Modules

This module supports:

- Project
- Brand
- Website
- AI
- OTA
- Operations
- Analytics
- User Experience
- Legal

These modules should consume Knowledge rather than duplicate it.

---

# Maintenance Rules

Before adding new information, ask the following questions:

1. Does this information already exist?
2. Which document owns this topic?
3. Can the existing document be updated instead?
4. Is a new knowledge domain being introduced?

Create a new document only when a new knowledge domain requires its own long-term ownership.

---

# Module Governance

The Knowledge module follows the following documentation standards:

- Documentation First
- Single Source of Truth (SSOT)
- One File, One Purpose
- Reference Before Duplication
- Clear Ownership Boundaries
- Factual and Verifiable Information
- Stable Cross-Module References

These principles ensure long-term maintainability and consistency across HotelAIOS.

---

# Notes

The Knowledge module is the factual foundation of HotelAIOS.

All downstream modules—including Website, AI, OTA, Operations, Analytics, and User Experience—should reference this module as the authoritative source of hotel information.

Whenever hotel information changes in the real world, the corresponding Knowledge document should be updated first before any dependent modules are modified.