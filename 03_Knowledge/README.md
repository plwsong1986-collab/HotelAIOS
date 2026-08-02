# Reference Layer

**Project:** HotelAIOS  
**Module:** Knowledge  
**Section:** Reference  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** 2026-07-31

---

# Purpose

This document serves as the authoritative entry point for the Reference Layer within the HotelAIOS Knowledge Module.

The Reference Layer defines standardized reference assets shared across the entire HotelAIOS platform, including master data, indexing standards, AI retrieval specifications, and ontology models.

It establishes reusable reference standards while maintaining clear ownership boundaries between business knowledge and reference knowledge.

This document is the Single Source of Truth (SSOT) for the Reference Layer.

---

# Overview

The Reference Layer provides standardized reference information that supports every Knowledge Domain.

Unlike Domain documents, which describe destination knowledge, travel knowledge, hotel knowledge, and guest-facing information, the Reference Layer defines reusable standards, semantic structures, metadata, classifications, indexing rules, retrieval specifications, and ontology models.

Every Knowledge Domain references this layer whenever shared standards are required.

The Reference Layer does not own business knowledge.

---

# Scope

The Reference Layer includes:

- Master Data
- Knowledge Index
- AI Retrieval
- Ontology
- Shared metadata
- Controlled vocabularies
- Classification standards
- Semantic models
- Knowledge architecture standards

The Reference Layer does not include:

- Destination knowledge
- Hotel information
- Travel guides
- Guest reviews
- Operational documentation
- Business workflows
- Commercial content

These remain owned by the corresponding Knowledge Domains.

---

# Architecture

The Reference Layer consists of four major components.

| Component | Purpose |
|----------|---------|
| 01_Master-Data | Defines reusable reference data, classifications, and controlled vocabularies |
| 02_Knowledge-Index | Defines indexing, metadata organization, and knowledge discovery standards |
| 03_AI-Retrieval | Defines AI retrieval, routing, prompt reference, and retrieval prioritization standards |
| 04_Ontology | Defines semantic entities, relationships, taxonomies, and synonym standards |

---

# Component Responsibilities

## Master Data

Provides globally reusable reference information including:

- Attractions Reference
- Facilities Reference
- Policies Reference
- Room Types Reference
- Services Reference
- Transportation Reference

Master Data standardizes reusable classifications and terminology shared across HotelAIOS.

---

## Knowledge Index

Provides standardized indexing structures including:

- Document Index
- Entity Index
- Keyword Index
- Knowledge Map

Knowledge Index enables semantic discovery, metadata consistency, and cross-domain navigation.

---

## AI Retrieval

Provides standardized retrieval guidance including:

- FAQ Routing
- Intent Routing
- Prompt Reference
- Retrieval Priority

AI Retrieval defines retrieval standards rather than AI implementations.

---

## Ontology

Provides semantic knowledge models including:

- Entities
- Relationships
- Synonyms
- Taxonomy

Ontology enables semantic interoperability, knowledge graphs, and enterprise knowledge management.

---

# Design Principles

The Reference Layer follows these principles:

- Single Source of Truth (SSOT)
- Reference-first architecture
- Implementation independence
- AI-ready organization
- RAG-ready structure
- Knowledge Graph compatibility
- Semantic consistency
- Enterprise governance
- Cross-domain reusability

Reference documents define standards rather than business knowledge.

---

# Relationship with Core

The Reference Layer extends the Core Knowledge Framework.

Core defines documentation standards.

Reference defines reusable knowledge standards.

---

# Relationship with Knowledge Domains

Knowledge Domains consume reference standards defined by the Reference Layer.

Reference documents should never duplicate Domain knowledge.

Knowledge Domains should reference shared standards maintained within the Reference Layer whenever possible.

---

# Relationship with AI Systems

The Reference Layer supports:

- AI Assistants
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Knowledge Graphs
- Intelligent Indexing
- Enterprise Search
- Future AI applications

The Reference Layer provides standardized semantic foundations while remaining implementation-independent.

---

# Single Source of Truth

The Reference Layer owns:

- Shared reference standards
- Master Data
- Knowledge indexing standards
- AI retrieval standards
- Ontology standards
- Controlled vocabularies
- Semantic models
- Reference architecture

The Reference Layer does not own:

- Business knowledge
- Destination content
- Operational procedures
- Hotel information
- Travel content
- Commercial documentation

Ownership remains with the corresponding Knowledge Domains.

---

# Directory Structure

```text
03_Reference/

├── architecture.md
├── README.md
│
├── 01_Master-Data
│   ├── README.md
│   ├── attractions.md
│   ├── facilities.md
│   ├── policies.md
│   ├── room-types.md
│   ├── services.md
│   └── transportation.md
│
├── 02_Knowledge-Index
│   ├── README.md
│   ├── document-index.md
│   ├── entity-index.md
│   ├── keyword-index.md
│   └── knowledge-map.md
│
├── 03_AI-Retrieval
│   ├── README.md
│   ├── faq-routing.md
│   ├── intent-routing.md
│   ├── prompt-reference.md
│   └── retrieval-priority.md
│
└── 04_Ontology
    ├── README.md
    ├── entities.md
    ├── relationships.md
    ├── synonyms.md
    └── taxonomy.md
```

---

# Maintenance

Review this component whenever:

- Reference standards evolve
- New reference components are introduced
- Knowledge architecture changes
- Documentation standards evolve
- SSOT ownership boundaries require clarification

Maintain consistency across all Reference documents.

---

# Notes

The Reference Layer is the semantic and architectural foundation of the HotelAIOS Knowledge Architecture.

It provides standardized reference information supporting every Knowledge Domain while ensuring consistency across AI Retrieval, Knowledge Index, Ontology, semantic search, enterprise knowledge management, and future intelligent applications.

This component should remain implementation-independent, AI Ready, RAG Ready, Knowledge Graph Ready, Ontology Ready, and suitable for long-term enterprise architectural governance.