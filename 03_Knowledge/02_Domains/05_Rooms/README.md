# Rooms Domain

**Project:** HotelAIOS  
**Module:** Knowledge  
**Section:** Domains  
**Domain:** Rooms  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** 2026-07-31

---

# Purpose

This document defines the scope, ownership, and architectural principles of the Rooms Domain.

The Rooms Domain serves as the authoritative source for structured knowledge related to hotel guest rooms, including room types, room features, amenities, occupancy, bedding configurations, accessibility, room views, and room-related policies.

This document establishes the Single Source of Truth (SSOT) for the Rooms Domain and provides a consistent architectural foundation for all downstream knowledge modules.

---

# Overview

The Rooms Domain organizes factual, implementation-independent, and AI-ready knowledge about hotel rooms and accommodations.

The domain focuses on stable information that helps guests understand room characteristics before, during, and after their stay.

The Rooms Domain does not contain booking availability, pricing, reservations, promotions, or operational status.

---

# Scope

The Rooms Domain includes knowledge related to:

- Room types
- Room amenities
- In-room features
- Bedding configurations
- Occupancy
- Accessibility
- Room views
- Room-related policies

The Rooms Domain does not include:

- Reservation information
- Room pricing
- Promotional offers
- Hotel facilities outside guest rooms
- Dining services
- Housekeeping operations
- Maintenance status
- Real-time room availability

These topics are maintained by their respective domains or operational systems.

---

# Domain Structure

The Rooms Domain currently consists of the following documents:

- README.md
- room-types.md
- amenities.md
- accessibility.md
- occupancy.md
- bedding.md
- views.md
- policies.md
- in-room-features.md

Additional documents may be introduced in future versions while maintaining the same architectural principles.

---

# Design Principles

The Rooms Domain follows the core design principles of HotelAIOS Documentation:

- Single Source of Truth (SSOT)
- AI Ready
- RAG Friendly
- Ontology Friendly
- Structured knowledge
- Implementation-independent
- Stable terminology
- Explicit ownership boundaries
- Cross-domain consistency

Knowledge should remain factual, verifiable, and free from subjective interpretation.

---

# Relationship to Other Domains

The Rooms Domain collaborates with other domains while maintaining clear ownership boundaries.

Examples include:

- Dining Domain for in-room dining references
- Transportation Domain for accessible transportation information
- Destination Policies Domain for accommodation-related regulations
- Core Knowledge for hotel location and contact information

Cross-domain references should point to authoritative documents rather than duplicate information.

---

# Standard Document Structure

Each document within the Rooms Domain should follow the standard HotelAIOS documentation template:

1. Header
2. Purpose
3. Overview
4. Scope
5. Core Information
6. Visitor Information
7. Accessibility
8. Guest Planning
9. Common Guest Questions
10. Keywords & Synonyms
11. Related Domains
12. Related Core Documents
13. Related Modules
14. Single Source of Truth
15. Maintenance
16. Notes

This standardized structure ensures consistency across the entire HotelAIOS knowledge base.

---

# AI Readiness

Documents within the Rooms Domain should:

- Support semantic search
- Support Retrieval-Augmented Generation (RAG)
- Use consistent terminology
- Avoid duplicated ownership
- Maintain factual accuracy
- Be implementation-independent
- Support ontology mapping
- Enable structured AI retrieval

---

# Single Source of Truth

The Rooms Domain owns structured knowledge related to hotel guest rooms and accommodations.

Each document within this domain owns a clearly defined area of knowledge.

Other domains should reference Rooms information rather than duplicate it.

Ownership boundaries must remain explicit and consistent.

---

# Maintenance

Review this domain whenever:

- Room classifications change
- Accommodation terminology evolves
- Domain boundaries change
- New room document types are introduced
- Cross-domain relationships are updated
- Knowledge architecture evolves

Ensure all documents remain consistent with the latest HotelAIOS documentation standards.

---

# Notes

This README defines the architectural foundation of the Rooms Domain.

All Rooms documents should follow the standards established here to ensure long-term consistency, maintainability, AI readiness, RAG compatibility, and ontology alignment throughout HotelAIOS Documentation v1.0.