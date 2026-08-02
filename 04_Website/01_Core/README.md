# Website Core

**Project:** HotelAIOS  
**Module:** Website  
**Section:** Core  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** 2026-07-31

---

# Purpose

This document serves as the authoritative entry point for the Website Core component within the HotelAIOS Website Module.

The Website Core defines the architectural principles, information architecture, navigation standards, content organization, user experience principles, URL strategy, metadata standards, and release governance used throughout the HotelAIOS website.

This document is the Single Source of Truth (SSOT) for the Website Core.

---

# Overview

The Website Core establishes the architectural foundation of the HotelAIOS website.

Unlike Website Domains, which define the specifications of individual pages, the Website Core defines the global standards that govern every page and component across the website.

Every Website Domain should follow the standards defined by this component.

---

# Scope

The Website Core includes:

- Website Architecture
- Navigation
- Page Hierarchy
- Content Strategy
- User Journey
- Design Principles
- URL Structure
- Metadata Standards
- Release Process

The Website Core does not include:

- Individual page specifications
- UI component implementations
- SEO implementation
- CSS
- JavaScript
- Backend services

These are owned by their corresponding components.

---

# Documents

The Website Core consists of the following documents.

| Document | Purpose |
|----------|---------|
| 01_site-architecture.md | Defines the overall website architecture |
| 02_navigation.md | Defines global navigation standards |
| 03_page-hierarchy.md | Defines website hierarchy and IA |
| 04_content-strategy.md | Defines content organization principles |
| 05_user-journey.md | Defines user journey architecture |
| 06_design-principles.md | Defines website design principles |
| 07_url-structure.md | Defines URL standards |
| 08_metadata.md | Defines page metadata standards |
| 09_release-process.md | Defines documentation and website release governance |

---

# Design Principles

The Website Core follows these principles:

- Single Source of Truth (SSOT)
- Information Architecture First
- User-Centered Design
- Content First
- Mobile First
- Accessibility First
- SEO Friendly
- AI Ready
- Scalable Architecture
- Consistent User Experience

---

# Relationship with Knowledge

The Website consumes knowledge from the Knowledge Module.

Knowledge remains the authoritative business source.

The Website transforms knowledge into user-facing experiences without duplicating ownership.

---

# Relationship with Website Domains

Website Domains define individual page specifications.

The Website Core defines the standards that every Website Domain must follow.

Website Domains should not redefine architectural principles established here.

---

# Relationship with Components

Website Components implement reusable UI building blocks.

Components follow the architectural principles defined by the Website Core.

The Website Core defines standards rather than implementation details.

---

# Relationship with SEO

The Website Core provides structural guidance.

The SEO component defines optimization standards.

SEO should extend—not replace—the architectural principles established by the Website Core.

---

# Single Source of Truth

The Website Core owns:

- Website architecture
- Navigation standards
- Information architecture
- User journey framework
- URL standards
- Metadata framework
- Design principles
- Release governance

The Website Core does not own:

- Individual pages
- UI components
- SEO implementation
- Frontend code
- Backend systems
- Business knowledge

Ownership remains with the corresponding modules.

---

# Directory Structure

```text
01_Core/

├── README.md
├── 01_site-architecture.md
├── 02_navigation.md
├── 03_page-hierarchy.md
├── 04_content-strategy.md
├── 05_user-journey.md
├── 06_design-principles.md
├── 07_url-structure.md
├── 08_metadata.md
└── 09_release-process.md
```

---

# Maintenance

Review this component whenever:

- Website architecture evolves
- Information architecture changes
- Navigation standards change
- User experience standards evolve
- Documentation standards change

Maintain consistency across all Website Core documents.

---

# Notes

The Website Core provides the architectural foundation for the entire HotelAIOS website.

It ensures consistency across Website Domains, Components, SEO, frontend implementation, and future website evolution.

This component should remain implementation-independent, scalable, AI Ready, SEO Ready, and suitable for long-term enterprise website governance.