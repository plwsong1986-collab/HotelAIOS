# Rooms

**Project:** HotelAIOS  
**Module:** Website  
**Layer:** Domains  
**Domain:** Rooms  
**Version:** 1.0  
**Status:** Draft

---

# Purpose

This document defines the website presentation structure for the Rooms domain.

The Rooms domain presents accommodation information to help guests understand available room options and make informed booking decisions.

---

# Responsibilities

The Rooms domain owns:

- Room page structure
- Room content presentation
- Room comparison experience
- Room detail navigation
- Booking guidance

It does not own room facts.

All factual room information must reference the Knowledge module.

---

# Scope

This domain covers:

- Room category pages
- Individual room pages
- Room features presentation
- Room image organization
- Room booking paths

---

# Structure

```text
Rooms/
│
├── README.md
│
├── 01_room-overview.md
├── 02_room-list.md
├── 03_room-detail.md
├── 04_room-features.md
├── 05_room-comparison.md
└── 06_booking-path.md
```

---

# Content Principles

Room pages should:

- Present information clearly
- Highlight guest benefits
- Use consistent terminology
- Provide accurate information
- Guide users toward booking

---

# Content Ownership

| Content | Owner |
|---------|-------|
| Room facts | Knowledge |
| Brand presentation | Brand |
| Page structure | Website |
| Booking process | Operations |

---

# User Experience Rules

Room pages should:

- Present key information early
- Use high-quality visual content
- Support comparison between room types
- Provide clear booking actions
- Work effectively across devices

---

# Progressive Expansion

Additional room-related pages should expand within this domain without changing the overall Website architecture.

---

# Related Documents

- `../README.md`
- `../../01_Core/01_site-architecture.md`
- `../../01_Core/03_page-hierarchy.md`
- `../../../03_Knowledge/01_Core/03_rooms.md`
- `../../../02_Brand/README.md`