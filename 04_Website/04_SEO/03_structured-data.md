# Structured Data

**Project:** HotelAIOS  
**Module:** Website  
**Layer:** SEO  
**Document:** Structured Data  
**Version:** 1.0  
**Status:** Draft

---

# Purpose

This document defines the structured data standards for the HotelAIOS website.

Structured data improves search engine understanding of website content, supports rich search results, and provides consistent semantic information across all website domains.

---

# Objectives

The Structured Data should:

- Standardize schema implementation
- Improve search result presentation
- Support semantic understanding
- Maintain structured information consistency
- Enable scalable structured data management

---

# Structured Data Structure

```text
Structured Data

├── Organization
│
├── Hotel
│
├── WebSite
│
├── WebPage
│
├── Breadcrumb
│
├── Article
│
├── FAQ
│
├── Image
│
└── Local Business
```

---

# Organization Schema

Organization schema should describe:

- Business name
- Brand identity
- Official website
- Contact information
- Logo
- Social profiles where applicable

Only one primary organization should represent the website.

---

# Hotel Schema

Hotel schema should describe:

- Hotel name
- Address
- Contact information
- Amenities
- Star rating where applicable
- Geographic location
- Check-in and check-out information where applicable

Hotel information should remain consistent across all related pages.

---

# WebSite Schema

The website schema should define:

- Website name
- Homepage URL
- Primary language
- Search capability where supported

Only one website schema should exist for the primary website.

---

# WebPage Schema

Each indexable page should define:

- Page name
- Description
- URL
- Primary topic
- Publication details where applicable

Page schema should accurately represent visible content.

---

# Breadcrumb Schema

Breadcrumb schema should:

- Reflect website hierarchy
- Match visible navigation
- Represent the current page accurately

Breadcrumb paths should remain consistent with website navigation.

---

# Article Schema

Article schema should be applied to:

- Blog articles
- Destination guides
- Travel tips
- Hotel news
- Other editorial content

Each article should include publication and update information where available.

---

# FAQ Schema

FAQ schema should:

- Represent visible questions and answers
- Match page content exactly
- Avoid hidden or generated content
- Remain synchronized with published FAQs

---

# Image Schema

Image schema should include:

- Image title where applicable
- Alternative description
- Image URL
- Associated page information

Images should accurately represent published content.

---

# Local Business Schema

Local business schema should define:

- Business location
- Contact details
- Opening information where applicable
- Geographic coordinates
- Available services

Business information should remain consistent across all structured data.

---

# Quality Principles

Structured data should:

- Match visible page content
- Remain technically valid
- Avoid duplicated entities
- Be updated with content changes
- Follow supported schema vocabulary

---

# Content Ownership

| Content | Owner |
|---------|-------|
| Schema strategy | SEO |
| Business information | Marketing |
| Editorial content | Content |
| Technical implementation | Engineering |

---

# Maintenance

Review this document when:

- Schema standards change
- Search engine guidance changes
- Website architecture changes
- New content types are introduced
- Business information changes

---

# Related Documents

- `README.md`
- `01_seo-overview.md`
- `02_metadata-standards.md`
- `04_content-optimization.md`
- `05_technical-seo.md`
- `06_internal-linking.md`
- `07_xml-sitemap.md`
- `08_seo-monitoring.md`
- `../02_Domains/Blog/README.md`