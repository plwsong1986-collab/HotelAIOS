# Booking

**Project:** HotelAIOS  
**Module:** Website  
**Layer:** Domains  
**Domain:** Booking  
**Version:** 1.0  
**Status:** Draft

---

# Purpose

This directory defines the website information architecture for the Booking domain.

The documents describe how the hotel booking journey is organized, presented, and navigated across the website. The Booking domain guides guests from availability search through reservation confirmation while maintaining a simple, consistent, and trustworthy booking experience.

This directory defines presentation only. Reservation rules, pricing logic, payment processing, and operational procedures belong to their respective Single Sources of Truth (SSOT).

---

# Objectives

The Booking domain should:

- Present the booking journey clearly
- Help guests complete reservations efficiently
- Explain booking-related information consistently
- Reduce uncertainty during reservation
- Maintain a consistent website experience

---

# Document Structure

| Order | Document | Purpose |
|--------|----------|---------|
| 01 | `01_booking-overview.md` | Introduces the Booking section |
| 02 | `02_availability-search.md` | Presents room availability search |
| 03 | `03_room-selection.md` | Presents room selection |
| 04 | `04_rate-plans.md` | Presents available rate plans |
| 05 | `05_guest-information.md` | Presents guest information entry |
| 06 | `06_payment.md` | Presents payment information |
| 07 | `07_booking-confirmation.md` | Presents reservation confirmation |
| 08 | `08_modify-booking.md` | Presents reservation modification |
| 09 | `09_cancellation.md` | Presents cancellation information |
| 10 | `10_booking-faq.md` | Answers common booking questions |

---

# Information Architecture

```text
Booking

├── Booking Overview
├── Availability Search
├── Room Selection
├── Rate Plans
├── Guest Information
├── Payment
├── Booking Confirmation
├── Modify Booking
├── Cancellation
└── Booking FAQ
```

---

# Content Principles

The Booking domain should:

- Keep the booking journey simple
- Present reservation information consistently
- Explain booking policies clearly
- Reduce guest uncertainty
- Reference factual information from the Knowledge module

---

# User Experience Principles

The Booking section should:

- Be easy to navigate
- Support step-by-step booking
- Support desktop and mobile devices
- Build guest confidence
- Minimize booking friction

---

# Content Ownership

| Content | Owner |
|---------|-------|
| Booking information | Knowledge |
| Brand presentation | Brand |
| Website structure | Website |
| Reservation policies | Operations |

---

# Navigation Relationships

The Booking domain should connect with:

- Home
- Rooms
- Services
- Experiences
- Contact

Internal navigation should support a continuous reservation journey.

---

# Maintenance

Review this directory when:

- Booking workflow changes
- Reservation policies change
- Navigation changes
- New booking features are introduced
- Content strategy is updated

---

# Related Documents

## Website

- `../../README.md`
- `../Rooms/README.md`
- `../Services/README.md`
- `../Experiences/README.md`

## Core

- `../../01_Core/03_page-hierarchy.md`
- `../../01_Core/04_content-strategy.md`
- `../../01_Core/05_user-journey.md`

## Knowledge

- `../../../03_Knowledge/02_Domains/Booking/README.md`