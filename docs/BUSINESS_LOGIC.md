# FinMang OS Business Logic

Version: 2.0
Status: Official (MVP Locked)

---

## Purpose

This document defines business rules, validations, calculations, and Islamic finance principles for the MVP.

---

## Core Principle (Amanah)

Every financial activity must be:

- **Intentional** — No automatic/unapproved entries.
- **Traceable** — Every change is logged.
- **Accountable** — User is responsible for all entries.
- **Measurable** — All calculations are transparent and reproducible.
- **Halal** — Track only permissible income/expenses (no Riba/interest-based income).

---

## Validation Rules (MVP)

### Transaction Validations
| Rule | Error |
| :--- | :--- |
| Amount must be > 0 | "Amount must be greater than zero." |
| Transaction date cannot be future | "Date cannot be in the future." |
| Category must exist | "Category not found." |
| Category type must match transaction type (INCOME/EXPENSE) | "Category type does not match transaction type." |
| Account must exist | "Account not found." |
| Account must be active | "Account is inactive." |

### Budget Validations
| Rule | Error |
| :--- | :--- |
| Budget amount must be > 0 | "Budget amount must be greater than zero." |
| Category must be EXPENSE type | "Budget cannot be assigned to INCOME category." |
| Start date must be before end date | "Start date must be before end date." |

### Asset/Debt Validations
| Rule | Error |
| :--- | :--- |
| Purchase price must be > 0 | "Purchase price must be greater than zero." |
| Current value must be >= 0 | "Current value cannot be negative." |
| Principal must be > 0 | "Principal must be greater than zero." |
| Interest rate must be >= 0 | "Interest rate cannot be negative." |
| Due date must be in future | "Due date must be in the future." |

---

## Calculation Formulas

### Account Balance
