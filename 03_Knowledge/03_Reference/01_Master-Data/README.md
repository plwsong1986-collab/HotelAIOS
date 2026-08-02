# Master Data

**Project:** HotelAIOS  
**Module:** Knowledge  
**Section:** Reference  
**Component:** Master Data  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** 2026-07-31

---

# Purpose

This document serves as the entry point for the Master Data component within the HotelAIOS Reference Layer.

Master Data provides standardized reference information shared across the HotelAIOS platform. It establishes authoritative reference definitions, classifications, controlled vocabularies, and reusable metadata that ensure consistency across all Knowledge Domains, AI systems, retrieval pipelines, and ontology models.

Master Data is the Single Source of Truth (SSOT) for reusable reference data.

---

# Overview

Master Data contains globally reusable reference information rather than business knowledge.

Every value maintained within this component should be stable, implementation-independent, and reusable across multiple modules.

Reference information should exist only once within HotelAIOS and be referenced wherever required.

---

# Scope

This component includes:

- Standard classifications
- Controlled vocabularies
- Shared metadata
- Reference identifiers
- Enumeration values
- Naming standards
- Domain-independent reference data
- Reusable taxonomies

This component does not include:

- Destination knowledge
- Travel information
- Hotel operations
- Guest guidance
- Business workflows
- Commercial content
- AI implementation logic

These remain owned by their corresponding modules.

---

# Documents

The Master Data component currently includes:

| Document | Purpose |
|----------|---------|
| attractions.md | Standard attraction classifications and reference terminology |
| facilities.md | Standard facility classifications and shared facility vocabulary |
| policies.md | Common policy reference classifications |
| room-types.md | Standard room type definitions and classifications |
| services.md | Standard service classifications and terminology |
| transportation.md | Standard transportation classifications and transport terminology |

---

# Design Principles

Master Data follows these principles:

- Single Source of Truth (SSOT)
- Reference-first architecture
- Enterprise consistency
- Controlled vocabulary
- Stable identifiers
- Reusable reference values
- AI-ready organization
- RAG-ready structure
- Ontology compatibility

Master Data defines standards rather than operational knowledge.

---

# Relationship with Other Components

Master Data supports:

- Knowledge Domains
- Knowledge Index
- AI Retrieval
- Ontology
- Search
- APIs
- Analytics

These components reference Master Data instead of maintaining duplicate definitions.

---

# Single Source of Truth

Master Data owns:

- Shared classifications
- Controlled vocabularies
- Standard reference values
- Reference terminology
- Reusable metadata
- Global reference definitions

Master Data does not own:

- Business knowledge
- Destination knowledge
- Operational procedures
- AI workflows
- Commercial information

Ownership remains with the corresponding modules.

---

# Maintenance

Review this component whenever:

- New reference standards are introduced
- Classification systems expand
- Controlled vocabularies change
- Documentation standards evolve
- SSOT ownership boundaries require clarification

Maintain consistency, stability, and backward compatibility whenever possible.

---

# Notes

Master Data provides the foundational reference standards for the entire HotelAIOS platform.

All reusable reference definitions should be maintained within this component and referenced by other modules instead of duplicated.

This component should remain implementation-independent, AI Ready, RAG Ready, Ontology Ready, and suitable for long-term enterprise knowledge governance.