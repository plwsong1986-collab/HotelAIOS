# Rooms

**Project:** HotelAIOS  
**Module:** Knowledge  
**Document:** Rooms  
**Version:** 2.0  
**Status:** Active  
**Last Updated:** 2026-07-31

---

# Purpose

This document defines the official room inventory and accommodation information for the hotel.

It serves as the **Single Source of Truth (SSOT)** for all room-related facts, including room categories, specifications, amenities, occupancy, accessibility, housekeeping standards, and in-room safety features.

Pricing, promotional descriptions, booking rules, and marketing content belong to other modules and should not be maintained here.

---

# Overview

Guest rooms are one of the hotel's primary assets.

This document provides standardized, factual, and maintainable room information for internal operations, AI systems, websites, OTA platforms, and other HotelAIOS modules.

Only stable and verifiable information should be maintained.

---

# Room Inventory

| Item | Description |
|------|-------------|
| Total Rooms | *To Be Defined* |
| Room Categories | *To Be Defined* |
| Maximum Occupancy | *To Be Defined* |

---

# Room Types

For each official room type, maintain the following information.

## Room Type Template

| Item | Description |
|------|-------------|
| Room Name | *To Be Defined* |
| Room Category | *To Be Defined* |
| Room Size | *To Be Defined* |
| Bed Configuration | *To Be Defined* |
| Maximum Occupancy | *To Be Defined* |
| View | *To Be Defined* |
| Floor | *To Be Defined* |

Repeat this template for every official room category operated by the hotel.

---

# Standard Amenities

Record amenities that are provided in every room.

Examples may include:

- Wi-Fi
- Air conditioning
- Heating
- Television
- Refrigerator
- Electric kettle
- Hair dryer
- Bathroom amenities
- Towels
- Slippers

Only include amenities that are consistently available across all applicable rooms.

Amenities available only in selected room types should be documented within those room specifications.

---

# Room Features

Record notable room characteristics, such as:

- Balcony
- Bathtub
- Smart room controls
- Soundproofing
- Oxygen support
- Mountain view
- Courtyard view
- Family layout

Describe features factually.

Avoid promotional or subjective language.

---

# Accessibility

Record accessibility information where applicable.

Examples include:

- Accessible room types
- Barrier-free bathrooms
- Wheelchair accessibility
- Accessible entrances
- Accessible facilities within guest rooms

Only include officially supported accessibility features.

---

# Housekeeping

Record the standard housekeeping information, such as:

- Daily housekeeping
- Linen replacement frequency
- Towel replacement policy
- Standard cleaning schedule

Detailed housekeeping procedures belong in the Operations module.

---

# In-Room Safety

Record standard in-room safety features, including:

- Smoke detector
- Fire extinguisher
- Emergency lighting
- Safe deposit box
- Emergency contact information

Only include officially installed safety equipment.

---

# Scope

This document should answer questions such as:

- What room types are available?
- How many guests can each room accommodate?
- What amenities are provided?
- What features distinguish each room?
- What accessibility options are available?

It should not answer pricing, promotions, availability, or reservation questions.

---

# Relationship with Other Knowledge Documents

This document owns all room-related information.

Other Knowledge documents define different aspects of the hotel:

- Hotel Overview defines the property's overall identity.
- Location explains where the hotel is located.
- Facilities describe shared public amenities.
- Services describe guest services.
- Experiences describe local activities.
- Policies define operational rules.
- FAQ answers common guest questions.

This document explains the hotel's accommodation.

Other documents explain the rest of the guest experience.

---

# Related Modules

This document may be referenced by:

- Website
- OTA
- AI
- Operations
- Analytics

All published room information should reference this document to ensure consistency.

---

# Related Documents

- README.md
- 01_hotel-overview.md
- 02_location.md
- 04_facilities.md
- 05_services.md
- 06_experiences.md
- 07_policies.md
- 08_faq.md

---

# Single Source of Truth

This document owns all official room-related information.

Examples include:

- Room inventory
- Official room names
- Room categories
- Room size
- Bed configuration
- Occupancy
- Standard amenities
- Room features
- Accessibility information
- In-room safety features

When conflicts occur, this document is the authoritative source for room information.

---

# Progressive Expansion

If room information becomes too extensive, this document may be expanded into a dedicated directory.

Example:

```text
03_rooms/

README.md
01_room-types.md
02_room-amenities.md
03_accessibility.md
04_housekeeping.md
05_room-features.md
```

Until such expansion is required, this document remains the single authoritative source for room information.

---

# Notes

This document is the authoritative source for accommodation information within HotelAIOS.

It should remain factual, concise, and operationally accurate.

Whenever room inventory, room specifications, amenities, accessibility features, or accommodation standards change, this document should be reviewed and updated.

Marketing descriptions, promotional copy, pricing, and booking conditions should remain in the Brand, Website, and OTA modules to preserve clear ownership boundaries.