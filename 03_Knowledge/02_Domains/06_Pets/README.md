# Pets Domain

**Project:** HotelAIOS  
**Module:** Knowledge  
**Section:** Domains  
**Domain:** Pets  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** 2026-07-31

---

# Purpose

The Pets Domain is the authoritative source for knowledge related to pets staying at or visiting hotel properties.

It provides structured, implementation-independent information about pet accommodation concepts, pet policies, and commonly supported companion animals. This domain supports AI assistants, guest services, reservation support, concierge teams, websites, and other downstream systems through a Single Source of Truth (SSOT).

---

# Overview

Many hotels accommodate guests traveling with pets under defined operational policies.

This domain organizes factual information about pet-related accommodations, common pet categories, and general hospitality terminology. It separates stable domain knowledge from hotel-specific operational rules, pricing, availability, or local regulations.

---

# Scope

This domain covers:

- Pet accommodation concepts
- General pet policies
- Common companion animal categories
- Hospitality terminology related to pets
- Typical guest questions regarding pets

This domain does not cover:

- Service animals or assistance animal regulations
- Veterinary care
- Medical advice
- Local government regulations
- Property-specific pricing
- Reservation availability
- Cleaning schedules
- Operational procedures

These topics are maintained by their respective domains or operational systems.

---

# Documents

| Document | Purpose |
|----------|---------|
| `pet-policy.md` | Defines general hotel pet policy concepts and terminology |
| `dog.md` | Defines knowledge related to dogs as companion animals in hospitality settings |
| `cat.md` | Defines knowledge related to cats as companion animals in hospitality settings |

---

# Domain Relationships

This domain may reference information from:

- Core documentation
- Rooms
- Destination Policies
- Travel FAQ

It may also be referenced by:

- AI
- Website
- OTA
- Reservation Support
- Guest Services
- Concierge
- Operations

---

# Design Principles

This domain follows these principles:

- Single Source of Truth (SSOT)
- One owner per concept
- Implementation independence
- AI-ready structure
- RAG-friendly organization
- Ontology-friendly terminology
- Explicit ownership boundaries
- Cross-document consistency

---

# Single Source of Truth

This domain owns factual knowledge related to:

- Companion pet accommodation concepts
- General hotel pet terminology
- Common pet categories
- General hospitality pet policies

This domain does not own:

- Room classifications
- Destination regulations
- Safety guidance
- Reservation policies
- Pricing
- Operational procedures
- Medical or veterinary information

Ownership of those topics remains with their respective domains.

---

# Maintenance

Review this domain whenever:

- Hospitality pet terminology evolves
- Industry accommodation practices change
- Cross-domain relationships are updated
- Documentation standards evolve

Maintain factual accuracy, consistent terminology, and explicit ownership boundaries.

---

# Notes

All documents within this domain should remain factual, structured, and implementation-independent.

The Pets Domain should not contain hotel-specific pricing, promotional content, reservation availability, operational workflows, medical advice, or local legal interpretations unless another domain explicitly delegates ownership.