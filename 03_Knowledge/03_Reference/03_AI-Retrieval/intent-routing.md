# Intent Routing

**Project:** HotelAIOS  
**Module:** Knowledge  
**Section:** Reference  
**Component:** AI Retrieval  
**Document:** Intent Routing  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** 2026-07-31

---

# Purpose

This document is the authoritative reference for intent routing standards within HotelAIOS.

It defines how user intents are identified, categorized, and mapped to authoritative knowledge sources across the HotelAIOS Knowledge Architecture.

This document is the Single Source of Truth (SSOT) for intent routing standards.

---

# Overview

Intent Routing establishes standardized intent classifications and routing principles that enable consistent knowledge retrieval across AI systems.

This document defines routing standards only and does not define intent detection algorithms or AI implementation details.

---

# Scope

This document includes:

- Intent classifications
- Intent taxonomy
- Domain routing
- Intent metadata
- Knowledge ownership mapping
- Routing priorities

This document does not include:

- AI models
- Natural language understanding
- Prompt engineering
- Business workflows
- Retrieval implementation

These remain owned by the corresponding components.

---

# Intent Classification

Typical intent categories may include:

- Information Request
- Recommendation Request
- Navigation Request
- Booking Inquiry
- Service Inquiry
- Facility Inquiry
- Transportation Inquiry
- Dining Inquiry
- Policy Inquiry
- Emergency Inquiry
- General Assistance

Additional intent categories may be introduced while maintaining backward compatibility.

---

# Routing Principles

Intent routing should be:

- Domain-first
- SSOT-based
- Deterministic
- Explainable
- Stable
- Reusable

Each intent should resolve to an authoritative knowledge source whenever possible.

---

# Routing Structure

Each intent route should support:

- Intent identifier
- Intent category
- Primary domain
- Secondary domain
- Related entities
- Metadata tags
- Routing priority
- Reference document

---

# Related References

This document relates to:

- FAQ Routing
- Prompt Reference
- Retrieval Priority
- Knowledge Index
- Ontology

---

# Related Components

Referenced by:

- AI Retrieval
- Knowledge Domains
- Search
- AI Assistants
- Documentation

---

# Single Source of Truth

This document owns:

- Intent routing standards
- Intent taxonomy
- Routing metadata
- Domain mapping rules

This document does not own:

- Intent recognition
- AI implementation
- Prompt engineering
- Knowledge content

Ownership remains with the corresponding components.

---

# Maintenance

Review this document whenever:

- New intent categories are introduced
- Knowledge architecture evolves
- Routing strategies expand
- Metadata standards change
- Documentation standards evolve

Maintain stable routing rules and consistent knowledge ownership.

---

# Notes

The Intent Routing component provides standardized intent routing across the HotelAIOS Knowledge Architecture.

It should remain implementation-independent, AI Ready, RAG Ready, Ontology Ready, and suitable for enterprise knowledge governance.