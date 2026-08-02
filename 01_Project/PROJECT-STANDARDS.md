# Project Standards

**Project:** HotelAIOS  
**Module:** Project  
**Document:** Project Standards  
**Version:** 2.0  
**Status:** Active  
**Last Updated:** 2026-07-31

---

# Purpose

This document defines the engineering standards that govern the HotelAIOS project.

It establishes a consistent framework for organizing, developing, reviewing, and maintaining documentation across all project modules.

These standards apply to every module within HotelAIOS and serve as the project's engineering baseline.

---

# Scope

This document applies to all current and future HotelAIOS modules, including but not limited to:

- Project
- Brand
- Knowledge
- Website
- AI
- OTA
- Media
- Operations
- Security
- Legal
- Development
- Deployment
- Integration
- Analytics
- User Experience

Every module should follow the same engineering principles regardless of its content.

---

# Core Principles

## One File, One Purpose

Each document should have one clearly defined responsibility.

Avoid combining multiple independent concepts into a single document.

If a document begins to serve multiple purposes, it should be refactored.

---

## Single Source of Truth (SSOT)

Every concept must have one authoritative owner.

Other documents should reference the original source instead of redefining it.

Duplication should be avoided whenever possible.

---

## Modular Architecture

HotelAIOS is organized as a collection of independent modules.

Each module owns its own content while remaining consistent with project-wide standards.

Modules should be loosely coupled and independently maintainable.

---

## Documentation First

Documentation defines the system before implementation.

Architecture, standards, and knowledge should be established before building websites, AI workflows, or software components.

---

## Long-Term Maintainability

Documentation should prioritize long-term clarity over short-term convenience.

Future contributors should be able to understand where information belongs and how it should evolve.

---

# File Standards

Every file should:

- Have one clear responsibility
- Use descriptive English names
- Avoid duplicated content
- Be easy to locate
- Be maintainable over time

Empty placeholder files should not remain in the repository.

---

# Naming Standards

## Directory Naming

Major project directories follow the project numbering convention:

```text
01_Project
02_Brand
03_Knowledge
...
15_UserExperience
99_Archive
```

Directory names use:

- Numeric prefix for stable ordering
- PascalCase naming
- One directory, one responsibility

---

## Document Naming

General documentation files should use:

- lowercase
- hyphen-separated
- descriptive filenames

Examples:

```text
brand-story.md
guest-promise.md
visual-guidelines.md
```

Community-standard filenames should be preserved where appropriate:

- README.md
- CHANGELOG.md
- VERSION.md
- TODO.md

---

# Document Header

Every documentation file should begin with:

```text
Project:
Module:
Document:
Version:
Status:
Last Updated:
```

This metadata provides consistency across the entire project.

---

# README Standard

Each module should contain one README.

The root repository also contains a project-level README that serves as the primary entry point for contributors.

A module README should explain:

- module purpose
- document responsibilities
- maintenance principles
- relationship with other modules

A README introduces a module.

It should not duplicate the detailed content of other documents.

---

# Module Lifecycle

Each module follows the same documentation lifecycle.

```text
Design
    ↓
Build
    ↓
Review
    ↓
Freeze
    ↓
Maintenance
```

A module should complete each stage before progressing to the next.

---

# Review Process

Every completed module should pass four review phases.

## Phase 1 — Structure Review

Verify:

- directory structure
- filenames
- numbering
- document ownership
- obsolete files removed

---

## Phase 2 — Reference Review

Verify:

- broken references
- outdated links
- duplicate navigation
- legacy references
- README consistency

---

## Phase 3 — Content Review

Verify:

- ownership boundaries
- duplicated concepts
- logical relationships
- documentation completeness
- Single Source of Truth (SSOT)

---

## Phase 4 — Standardization Review

Verify:

- formatting
- terminology
- document headers
- writing consistency
- engineering quality

---

# Freeze Policy

A module may enter Freeze only when:

- review phases are complete
- responsibilities are clearly defined
- duplicate concepts have been removed
- documentation structure is stable

After Freeze:

- content may continue to evolve
- factual corrections are encouraged
- architectural changes should be minimized

Freeze represents architectural stability rather than permanent immutability.

---

# Cross-Module Principles

Modules should reference one another rather than duplicate information.

Examples:

- Website references Brand.
- AI references Knowledge.
- OTA references Operations.
- Operations references Knowledge where appropriate.

Shared concepts should always have one authoritative owner.

---

# Repository Maintenance

Before creating a new document, ask:

1. Does this concept already exist?
2. Which document owns this concept?
3. Can an existing document be expanded instead?

Create a new document only when a genuinely new responsibility is introduced.

---

# Project Governance

The `01_Project` module governs the project itself.

It provides the governance framework for every module within the repository.

It defines:

- project standards
- development workflow
- roadmap
- version management
- release history
- project maintenance

Business and domain knowledge belong in their respective modules.

---

# Engineering Philosophy

HotelAIOS treats documentation as a core engineering asset.

Well-designed documentation improves collaboration, reduces duplication, and enables long-term scalability.

Every document should make the project easier to understand, maintain, and extend.

---

# Module Architecture

HotelAIOS adopts the official Module Architecture Standard documented in `01_Project/08_module-architecture.md`.

All major modules should follow this standard unless an approved exception has been documented.

The standard defines:

- Module structure
- Layer responsibilities
- Single Source of Truth (SSOT)
- Progressive Expansion
- Review workflow
- Naming conventions
- Module ownership

Every new module should be designed according to the Module Architecture Standard before implementation begins.

Refer to `01_Project/08_module-architecture.md` for the complete architecture specification and implementation guidelines.

---

# Related Documents

- README.md
- PROJECT-STRUCTURE.md
- DOCUMENT-LIFECYCLE.md
- ROADMAP.md
- VERSION.md
- CHANGELOG.md
- RELEASE-NOTES.md
- 08_module-architecture.md