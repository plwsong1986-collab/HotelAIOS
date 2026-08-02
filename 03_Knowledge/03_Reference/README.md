# Reference Layer

**Project:** HotelAIOS  
**Module:** Knowledge  
**Section:** Reference  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** 2026-07-31

---

# Purpose

This document serves as the entry point for the HotelAIOS Reference Layer.

The Reference Layer provides standardized reference information shared across the entire HotelAIOS Knowledge Module. It establishes common definitions, classifications, metadata, indexing standards, AI retrieval specifications, and ontology models that support every Knowledge Domain.

The Reference Layer is the authoritative Single Source of Truth (SSOT) for reusable reference information.

---

# Overview

Unlike Domain documents, which describe destination and business knowledge, the Reference Layer defines standardized reference assets used across multiple domains.

Reference documents provide common standards rather than operational knowledge.

Every Domain may consume Reference information.

Reference documents do not duplicate Domain ownership.

---

# Components

The Reference Layer consists of the following components.

| Component | Description |
|-----------|-------------|
| 01_Master-Data | Shared master data, controlled vocabularies, classifications, identifiers, and standardized values |
| 02_Knowledge-Index | Knowledge catalog, metadata registry, indexing standards, and cross-reference definitions |
| 03_AI-Retrieval | AI retrieval standards, metadata, chunking references, retrieval rules, and semantic search support |
| 04_Ontology | Entity models, semantic relationships, taxonomies, vocabularies, and knowledge graph foundations |

---

# Design Principles

The Reference Layer follows these principles:

- Single Source of Truth (SSOT)
- Reference-first architecture
- Enterprise consistency
- Implementation independence
- AI-ready organization
- RAG-ready structure
- Ontology-ready design
- Semantic interoperability
- Cross-domain reusability

Reference documents define reusable standards instead of business knowledge.

---

# Relationship with Core

Core defines documentation standards.

Reference defines reusable knowledge standards.

---

# Relationship with Domains

Domains reference shared standards maintained within the Reference Layer.

Reference documents do not own destination knowledge, travel knowledge, hotel knowledge, or operational information.

---

# Reference Ownership

The Reference Layer owns:

- Standard definitions
- Controlled vocabularies
- Metadata
- Classification systems
- Reference identifiers
- Knowledge indexing standards
- Retrieval standards
- Ontology models

The Reference Layer does not own:

- Destination knowledge
- Cultural knowledge
- Transportation knowledge
- Dining knowledge
- Guest Reviews
- Travel Guides
- Operational procedures
- Commercial information

These remain owned by the corresponding Knowledge Domains.

---

# Directory Structure

```text
03_Reference/

├── architecture.md
├── README.md
├── 01_Master-Data/
├── 02_Knowledge-Index/
├── 03_AI-Retrieval/
└── 04_Ontology/
```

---

# Single Source of Truth

This directory is the authoritative source for all reusable reference information within HotelAIOS.

All shared standards should be maintained here and referenced by Domains rather than duplicated.

---

# Maintenance

Review this layer whenever:

- Reference standards expand
- New metadata standards are introduced
- Knowledge architecture evolves
- AI retrieval standards change
- Ontology models expand
- SSOT ownership boundaries require clarification

Maintain consistency across all reference documents.

---

# Notes

The Reference Layer forms the foundation of the HotelAIOS Knowledge Architecture.

It enables consistent terminology, standardized metadata, semantic interoperability, AI retrieval, and ontology management across the entire HotelAIOS platform.

This layer should remain implementation-independent, AI Ready, RAG Ready, Ontology Ready, and suitable for long-term enterprise knowledge governance.