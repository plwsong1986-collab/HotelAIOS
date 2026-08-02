# Project Structure

**Project:** HotelAIOS  
**Module:** Project  
**Document:** Project Structure  
**Version:** 1.0  
**Status:** Active  
**Last Updated:** 2026-07-31

---

# Purpose

This document defines the official repository structure of the HotelAIOS project.

It specifies the responsibilities of every top-level module and establishes the organizational framework used throughout the repository.

This document serves as the Single Source of Truth (SSOT) for project organization and directory ownership.

---

# Design Principles

The HotelAIOS repository is designed according to the following principles.

- Modular Architecture
- One Directory, One Responsibility
- One File, One Purpose
- Documentation First
- Single Source of Truth (SSOT)
- Long-Term Maintainability
- Progressive Expansion

The repository structure should remain stable as the project evolves.

---

# Repository Layout

```text
HotelAIOS/

01_Project/
02_Brand/
03_Knowledge/
04_Website/
05_AI/
06_OTA/
07_Media/
08_Operations/
09_Security/
10_Legal/
11_Development/
12_Deployment/
13_Integration/
14_Analytics/
15_UserExperience/

99_Archive/
```

---

# Module Responsibilities

## 01_Project

Project governance, engineering standards, roadmap, lifecycle management, release management, and repository governance.

---

## 02_Brand

Brand identity, positioning, messaging, storytelling, visual identity, logos, and brand guidelines.

---

## 03_Knowledge

Hospitality knowledge, operational knowledge, business reference information, and domain documentation.

---

## 04_Website

Website architecture, information architecture, content strategy, SEO, user interface documentation, and website governance.

---

## 05_AI

AI architecture, AI agents, prompt management, memory, knowledge integration, workflows, and AI governance.

---

## 06_OTA

OTA integration, reservation synchronization, inventory synchronization, pricing, channel management, and OTA governance.

---

## 07_Media

Images, videos, photography, logos, icons, marketing assets, screenshots, and media management.

---

## 08_Operations

Operational procedures, SOPs, workflows, service management, incident management, monitoring, and operational governance.

---

## 09_Security

Identity management, application security, infrastructure security, access control, risk management, and security governance.

---

## 10_Legal

Privacy, compliance, contracts, licensing, intellectual property, legal documentation, and governance.

---

## 11_Development

Development standards, coding standards, APIs, testing, CI/CD, architecture, and engineering documentation.

---

## 12_Deployment

Deployment planning, environments, release process, rollback strategy, deployment validation, and deployment governance.

---

## 13_Integration

API integration, webhooks, messaging, third-party systems, event-driven architecture, and integration governance.

---

## 14_Analytics

Analytics architecture, KPIs, dashboards, reporting, metrics, visualization, and analytics governance.

---

## 15_UserExperience

User journeys, interaction design, accessibility, usability, personalization, UX research, feedback, and experience governance.

---

## 99_Archive

Historical documents retained for reference.

Archived content is read-only and should not be used as the authoritative source for active project development.

---

# Directory Organization Rules

The repository follows these directory standards.

- One directory owns one business responsibility.
- Directories should not overlap in ownership.
- Cross-module dependencies should use references instead of duplication.
- Every major module should contain exactly one README.
- Resource directories should not contain unnecessary documentation.

---

# Numbering Convention

Major modules use a numeric prefix to provide stable ordering.

Example:

```text
01_Project
02_Brand
03_Knowledge
...
15_UserExperience
99_Archive
```

The numeric prefix represents repository organization only.

It does not indicate implementation priority or business importance.

---

# Expansion Policy

New modules may be introduced when a genuinely new responsibility is identified.

When expanding the repository:

- Preserve existing numbering whenever possible.
- Avoid renumbering released modules.
- Define clear ownership before adding a new module.
- Update this document whenever the repository structure changes.

---

# Ownership Principles

Each module owns its own documentation.

Examples:

- Brand owns brand identity.
- Knowledge owns operational knowledge.
- Website owns website content.
- AI owns AI workflows.
- OTA owns OTA integrations.

Other modules should reference these sources rather than duplicate them.

---

# Relationship with Module Architecture

This document defines **what** modules exist and **what** they own.

The internal organization of each module is defined separately in:

`01_Project/08_module-architecture.md`

The Module Architecture Standard specifies:

- Layer structure
- Folder organization
- Progressive Expansion
- Documentation ownership
- Review workflow

---

# Related Documents

- README.md
- PROJECT-STANDARDS.md
- DOCUMENT-LIFECYCLE.md
- ROADMAP.md
- VERSION.md
- CHANGELOG.md
- RELEASE-NOTES.md
- 08_module-architecture.md