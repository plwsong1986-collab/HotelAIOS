# Services

**Project:** HotelAIOS  
**Module:** Website  
**Layer:** Domains  
**Domain:** Services  
**Version:** 1.0  
**Status:** Draft

---

# Purpose

This directory defines the website information architecture for the Services domain.

The documents describe how hotel services are organized, presented, and navigated across the website. The Services domain helps guests understand available services before and during their stay while maintaining a consistent experience throughout the website.

This directory defines presentation only. Service policies, operational procedures, and service details belong to their respective Single Sources of Truth (SSOT).

---

# Objectives

The Services domain should:

- Present hotel services clearly
- Help guests discover available services
- Explain how services can be accessed
- Support guest decision-making
- Maintain consistent navigation and presentation

---

# Document Structure

| Order | Document | Purpose |
|--------|----------|---------|
| 01 | `01_services-overview.md` | Introduces the Services section |
| 02 | `02_front-desk.md` | Presents front desk services |
| 03 | `03_concierge.md` | Presents concierge services |
| 04 | `04_room-service.md` | Presents room service |
| 05 | `05_housekeeping.md` | Presents housekeeping services |
| 06 | `06_laundry.md` | Presents laundry services |
| 07 | `07_transportation.md` | Presents transportation services |
| 08 | `08_business-services.md` | Presents business support services |
| 09 | `09_guest-assistance.md` | Presents guest assistance services |
| 10 | `10_service-guide.md` | Explains service access and policies |

---

# Information Architecture

```text
Services

├── Services Overview
├── Front Desk
├── Concierge
├── Room Service
├── Housekeeping
├── Laundry
├── Transportation
├── Business Services
├── Guest Assistance
└── Service Guide
```

---

# Content Principles

The Services domain should:

- Focus on guest needs
- Present services consistently
- Keep information easy to understand
- Explain service availability clearly
- Reference factual information from the Knowledge module

---

# User Experience Principles

The Services section should:

- Be easy to navigate
- Help guests quickly locate services
- Support desktop and mobile devices
- Encourage service discovery
- Minimize guest effort

---

# Content Ownership

| Content | Owner |
|---------|-------|
| Service information | Knowledge |
| Brand presentation | Brand |
| Website structure | Website |
| Operational policies | Operations |

---

# Navigation Relationships

The Services domain should connect with:

- Home
- Rooms
- Dining
- Facilities
- Experiences
- Contact

Internal navigation should guide guests naturally between related services.

---

# Maintenance

Review this directory when:

- New services are introduced
- Existing services change
- Website navigation changes
- Operational policies change
- Content strategy is updated

---

# Related Documents

## Website

- `../../README.md`
- `../Home/README.md`
- `../Rooms/README.md`
- `../Dining/README.md`
- `../Facilities/README.md`
- `../Experiences/README.md`

## Core

- `../../01_Core/03_page-hierarchy.md`
- `../../01_Core/04_content-strategy.md`
- `../../01_Core/05_user-journey.md`

## Knowledge

- `../../../03_Knowledge/02_Domains/Services/README.md`