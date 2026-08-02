# URL Structure

**Project:** HotelAIOS  
**Module:** Website  
**Section:** Core  
**Document:** URL Structure  
**Version:** 1.0  
**Status:** Draft  
**Last Updated:** 2026-07-31

---

# Purpose

This document defines the URL structure standards for the HotelAIOS website.

It establishes consistent URL conventions, hierarchy, naming rules, governance, and ownership boundaries to improve usability, SEO, maintainability, and AI-assisted content discovery.

This document is the Single Source of Truth (SSOT) for website URL standards.

---

# Overview

A well-structured URL system improves navigation, discoverability, search engine indexing, and long-term maintainability.

URLs should reflect the website information architecture rather than implementation details.

---

# Scope

This document includes:

- URL hierarchy
- URL naming conventions
- Path structure
- Canonical URL standards
- Localization considerations
- Redirect strategy
- URL governance

This document does not include:

- Server configuration
- Routing implementation
- Backend frameworks
- SEO implementation
- Analytics configuration

These remain owned by their corresponding modules.

---

# URL Principles

URLs should be:

- Human-readable
- Stable
- Predictable
- Hierarchical
- SEO Friendly
- AI Ready
- Implementation-independent
- Easy to maintain

URLs should remain consistent throughout the website lifecycle.

---

# URL Naming Rules

URLs should:

- Use lowercase letters
- Use hyphens (-) to separate words
- Avoid spaces
- Avoid underscores
- Avoid unnecessary parameters
- Avoid implementation-specific identifiers
- Remain concise and descriptive

Example:

```text
/rooms/deluxe-suite
```

---

# URL Hierarchy

Typical URL hierarchy:

```text
/
/rooms/
/rooms/{room-type}
/dining/
/experiences/
/facilities/
/services/
/about/
/blog/
/contact/
```

The hierarchy should reflect the Information Architecture defined by the Website Core.

---

# Canonical URLs

Every public page should have:

- One canonical URL
- Consistent internal references
- Stable URL ownership
- Clear parent hierarchy

Canonicalization implementation belongs to the SEO module.

---

# Localization

Localized websites should maintain:

- Consistent URL patterns
- Predictable language prefixes (if applicable)
- Stable page hierarchy
- Equivalent page relationships across languages

Localization should not change the underlying information architecture.

---

# Redirect Strategy

Redirects should:

- Preserve user experience
- Preserve SEO value
- Avoid redirect chains
- Maintain canonical ownership
- Be documented when structural changes occur

Implementation details are outside the scope of this document.

---

# Relationship with Navigation

Navigation references URLs defined by this document.

Navigation should not introduce inconsistent URL structures.

---

# Relationship with SEO

SEO defines optimization strategies.

This document defines the structural standards upon which SEO is built.

---

# Single Source of Truth

This document owns:

- URL standards
- URL hierarchy
- Naming conventions
- URL governance
- Structural consistency

This document does not own:

- Routing implementation
- Server configuration
- SEO implementation
- Backend architecture

Ownership remains with the corresponding modules.

---

# Maintenance

Review this document whenever:

- Website architecture changes
- Information architecture evolves
- SEO strategy changes
- Documentation standards evolve

Maintain stable and predictable URL structures.

---

# Notes

The URL Structure document provides the foundational standards for all website URLs within HotelAIOS.

It ensures consistency across Website Domains, Navigation, SEO, frontend implementation, AI-assisted retrieval, and long-term enterprise website governance.