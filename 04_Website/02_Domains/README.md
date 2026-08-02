# Website Domains

**Project:** HotelAIOS  
**Module:** Website  
**Section:** Domains  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** 2026-07-31

---

# Purpose

This document serves as the authoritative entry point for the Website Domains component within the HotelAIOS Website Module.

Website Domains define the specifications, structure, content organization, and functional responsibilities of every major section of the HotelAIOS website.

This document is the Single Source of Truth (SSOT) for Website Domains.

---

# Overview

Website Domains organize the HotelAIOS website into logical business sections.

Each Domain represents a user-facing website area with clearly defined responsibilities, page structures, navigation relationships, and content boundaries.

Website Domains consume knowledge from the Knowledge Module while following the architectural standards established by the Website Core.

---

# Scope

Website Domains include:

- Home
- Rooms
- Dining
- Experiences
- Facilities
- Services
- Guest Services
- Booking
- About
- Blog
- Contact

Website Domains do not include:

- Website architecture
- Navigation standards
- UI components
- SEO implementation
- Frontend implementation
- Business knowledge

These remain owned by their corresponding modules.

---

# Documents

The Website Domains component consists of the following documents.

| Document | Purpose |
|----------|---------|
| home.md | Defines the Home page specification |
| rooms.md | Defines the Rooms section specification |
| dining.md | Defines the Dining section specification |
| experiences.md | Defines the Experiences section specification |
| facilities.md | Defines the Facilities section specification |
| services.md | Defines the Services section specification |
| guest-services.md | Defines the Guest Services section specification |
| booking.md | Defines the Booking experience specification |
| about.md | Defines the About section specification |
| blog.md | Defines the Blog section specification |
| contact.md | Defines the Contact section specification |

---

# Design Principles

Website Domains follow these principles:

- Single Source of Truth (SSOT)
- Content First
- User-centered Design
- Information Architecture First
- Mobile First
- Accessibility First
- SEO Friendly
- AI Ready
- Consistent User Experience
- Scalable Architecture

---

# Relationship with Knowledge

Website Domains present business knowledge maintained by the Knowledge Module.

Knowledge remains the authoritative business source.

Website Domains should reference Knowledge rather than duplicate ownership.

---

# Relationship with Website Core

The Website Core defines:

- Architecture
- Navigation
- Information Architecture
- URL Structure
- Metadata Standards
- Design Principles

Website Domains implement these standards and should not redefine them.

---

# Relationship with Components

Website Components provide reusable UI building blocks.

Website Domains assemble Components into complete user-facing pages while preserving architectural consistency.

---

# Relationship with SEO

The SEO component defines optimization standards.

Website Domains should follow those standards while focusing on page structure, content organization, and user experience.

---

# Single Source of Truth

Website Domains own:

- Page specifications
- Section responsibilities
- Page structure
- Content organization
- Functional boundaries
- User-facing experiences

Website Domains do not own:

- Business knowledge
- Website architecture
- UI components
- SEO implementation
- Frontend implementation

Ownership remains with the corresponding modules.

---

# Directory Structure

```text
02_Domains/

├── README.md
├── home.md
├── rooms.md
├── dining.md
├── experiences.md
├── facilities.md
├── services.md
├── guest-services.md
├── booking.md
├── about.md
├── blog.md
└── contact.md
```

---

# Maintenance

Review this component whenever:

- New website sections are introduced
- Website architecture evolves
- Information architecture changes
- User experience standards evolve
- Documentation standards change

Maintain consistency across all Website Domain documents.

---

# Notes

The Website Domains component defines the complete structure of the HotelAIOS website.

It provides standardized page specifications that integrate Knowledge, Website Core, Components, and SEO into a unified, scalable, AI-ready, and enterprise-governed website architecture.