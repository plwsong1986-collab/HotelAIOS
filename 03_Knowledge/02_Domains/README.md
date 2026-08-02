# Domains

**Project:** HotelAIOS  
**Module:** Knowledge  
**Section:** Domains  
**Document:** README  
**Version:** 1.0  
**Status:** Active  
**Last Updated:** 2026-07-31

---

# Purpose

The Domains section extends the core hotel knowledge maintained in the Knowledge module.

It provides structured knowledge about specific subject areas that support guest inquiries, AI retrieval, website content, and operational reference.

Unlike the Core documents, Domain documents focus on individual knowledge domains rather than the hotel itself.

---

# Overview

The Core module answers questions about the hotel.

The Domains section answers questions surrounding the hotel and guest experience.

Examples include:

- Local attractions
- Transportation
- Dining
- Local culture
- Pet travel
- Room guides
- Guest reviews
- Travel guides
- Frequently asked questions

Each domain is maintained independently while following the same documentation standards.

---

# Scope

Domain documents provide factual and maintainable information related to a single topic.

Typical domains include:

- Attractions
- Culture
- Dining
- FAQ
- Guides
- Pets
- Policies
- Reviews
- Rooms
- Transportation

Additional domains may be introduced as the project expands.

---

# Relationship with Core

The relationship between Core and Domains is clearly separated.

| Core | Domains |
|------|----------|
| Hotel identity | Destination knowledge |
| Hotel facilities | Local information |
| Hotel services | Travel assistance |
| Hotel policies | Topic-specific guidance |
| Hotel facts | Extended guest knowledge |

Core owns hotel facts.

Domains provide supporting knowledge.

---

# Directory Structure

```text
02_Domains/

README.md

Attractions/
Culture/
Dining/
FAQ/
Guides/
Pets/
Policies/
Reviews/
Rooms/
Transportation/
```

Each directory represents an independent knowledge domain.

Every domain may contain its own README and one or more documents.

---

# Documentation Principles

## One Domain, One Responsibility

Each directory owns one knowledge domain.

Avoid mixing unrelated topics.

---

## Single Source of Truth (SSOT)

Every knowledge topic has one authoritative document.

Other documents should reference it instead of duplicating content.

---

## Progressive Expansion

A domain should begin with a small number of documents.

As knowledge grows, additional documents may be introduced without changing ownership.

Example:

```text
Dining/

README.md

breakfast.md
coffee.md
tea.md
snacks.md
drinks.md
```

---

## Reference Before Duplication

Knowledge should be shared through references rather than copied across multiple documents.

This improves maintainability and AI retrieval accuracy.

---

# Related Modules

The Domains section supports:

- Brand
- Website
- AI
- OTA
- Operations
- Media
- User Experience

These modules may consume Domain knowledge while preserving the Core module as the authoritative source for hotel facts.

---

# Relationship with Reference

The Domains section defines structured knowledge.

The Reference section transforms this knowledge into standardized datasets for AI retrieval, indexing, and integration.

In general:

- Core defines hotel facts.
- Domains organize extended knowledge.
- Reference provides structured master data.

---

# Maintenance Rules

Before creating a new domain, ask:

1. Does this topic already belong to an existing domain?
2. Can an existing document be expanded?
3. Is the new domain expected to grow over time?

Only introduce a new domain when it represents a distinct long-term knowledge area.

---

# Notes

The Domains section is designed to grow continuously as HotelAIOS evolves.

New destinations, transportation options, dining information, travel guidance, and guest resources may be added over time.

All Domain documents should follow the governance principles established by the HotelAIOS documentation system.