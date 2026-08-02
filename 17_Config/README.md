# AIGOS Configuration Center

**Project:** HotelAIOS / AIGOS  
**Module:** Configuration  
**Version:** 1.0  
**Status:** Active  
**Last Updated:** 2026-08-02

---

# Purpose

The Configuration Center defines and manages all hotel, inn, homestay, and accommodation property configurations used by AIGOS.

It enables multiple properties to coexist within a single repository while preserving strict data isolation, stable identifiers, deletion protection, and long-term maintainability.

The Configuration Center is designed to support the following operating principle:

> New properties may be added, copied, configured, or activated without overwriting or deleting any existing property data.

---

# Core Principle

AIGOS uses a multi-property configuration model.

Each hotel, inn, homestay, guesthouse, hostel, resort, or accommodation property must have:

- A unique property identifier
- An independent configuration directory
- Independent brand settings
- Independent website settings
- Independent SEO and GEO settings
- Independent OTA settings
- Independent lifecycle status
- Deletion protection enabled by default

Existing property information must remain preserved unless the repository owner explicitly authorizes deletion of a specific property.

---

# Directory Structure

```text
17_Config/
├── README.md
├── properties.yaml
└── properties/
    ├── _template/
    │   ├── hotel.yaml
    │   ├── brand.yaml
    │   ├── website.yaml
    │   ├── seo.yaml
    │   └── ota.yaml
    └── {property_id}/
        ├── hotel.yaml
        ├── brand.yaml
        ├── website.yaml
        ├── seo.yaml
        └── ota.yaml