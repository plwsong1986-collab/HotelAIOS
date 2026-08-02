# Retrieval Priority

**Project:** HotelAIOS  
**Module:** Knowledge  
**Section:** Reference  
**Component:** AI Retrieval  
**Document:** Retrieval Priority  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** 2026-07-31

---

# Purpose

This document is the authoritative reference for retrieval priority standards within HotelAIOS.

It defines how authoritative knowledge sources are prioritized during retrieval while preserving Single Source of Truth (SSOT) ownership across the HotelAIOS Knowledge Architecture.

This document is the Single Source of Truth (SSOT) for retrieval prioritization standards.

---

# Overview

Retrieval Priority establishes standardized rules for selecting the most authoritative knowledge source when multiple related references are available.

The objective is to ensure retrieval consistency, minimize duplicated knowledge, and maintain predictable AI behavior.

This document defines prioritization standards rather than retrieval algorithms.

---

# Scope

This document includes:

- Retrieval priority levels
- Knowledge source precedence
- Cross-domain priority rules
- Reference hierarchy
- Metadata priorities
- Conflict resolution guidance

This document does not include:

- AI implementation
- Ranking algorithms
- Vector search configuration
- Prompt engineering
- Business knowledge

These remain owned by the corresponding components.

---

# Priority Principles

Knowledge retrieval should follow these principles:

- Single Source of Truth first
- Domain ownership first
- Reference before duplication
- Stable precedence
- Deterministic selection
- Explainable routing

Knowledge should always be retrieved from its authoritative source whenever possible.

---

# Priority Hierarchy

Recommended retrieval precedence:

1. Authoritative SSOT document
2. Primary Domain document
3. Reference Layer document
4. Cross-domain reference
5. Related supporting document
6. Fallback reference

Projects may refine this hierarchy while preserving SSOT ownership.

---

# Priority Metadata

Each retrieval rule should support:

- Priority level
- Knowledge owner
- Reference source
- Related domains
- Metadata tags
- Confidence guidance
- Conflict resolution reference

---

# Conflict Resolution

When multiple knowledge sources exist:

- Prefer the authoritative SSOT.
- Avoid duplicate knowledge.
- Preserve documented ownership boundaries.
- Use cross-references instead of replicated content.
- Escalate to architecture governance when ownership conflicts cannot be resolved.

---

# Related References

This document relates to:

- FAQ Routing
- Intent Routing
- Prompt Reference
- Knowledge Index
- Ontology

---

# Related Components

Referenced by:

- AI Retrieval
- Knowledge Domains
- Search
- AI Assistants
- Enterprise Knowledge Management

---

# Single Source of Truth

This document owns:

- Retrieval priority standards
- Retrieval precedence hierarchy
- Priority metadata
- Conflict resolution guidance

This document does not own:

- Knowledge content
- Retrieval implementation
- AI models
- Business logic

Ownership remains with the corresponding components.

---

# Maintenance

Review this document whenever:

- Knowledge architecture evolves
- New domains are introduced
- Retrieval strategy changes
- Metadata standards evolve
- Documentation standards change

Maintain stable prioritization rules and consistent SSOT ownership.

---

# Notes

The Retrieval Priority component provides standardized retrieval precedence across the HotelAIOS Knowledge Architecture.

It should remain implementation-independent, AI Ready, RAG Ready, Ontology Ready, and suitable for enterprise knowledge governance.