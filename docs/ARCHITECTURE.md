# FinMang OS Architecture

Version: 1.0
Status: Draft

---

# Purpose

This document defines the technical architecture of FinMang OS.

It describes how the system is organized, how components interact, and the architectural principles that guide implementation.

---

# Architecture Principles

- Modular design
- Loose coupling
- High cohesion
- Domain-driven development
- Maintainability first
- Security by design
- Testability
- Scalability

---

# System Layers

1. Presentation Layer
2. Application Layer
3. Domain Layer
4. Infrastructure Layer
5. Data Layer

---

# Core Modules

- Financial Engine
- Budget Engine
- Daily Log
- Asset Management
- Debt Management
- Automation Engine
- Reporting
- Analytics
- Archive

---

# Documentation Structure

- docs/ — Official project documentation
- database/ — Database design
- automation/ — Automation workflows
- assets/ — Images, icons and branding
- archive/ — Historical records

---

# Future Sections

- Technology Stack
- Folder Structure
- Database Architecture
- API Architecture
- Frontend Architecture
- Deployment Architecture
- Security Architecture
---

# Module Responsibilities

## Financial Engine
- Manage accounts
- Record transactions
- Calculate balances

## Budget Engine
- Create budgets
- Track budget usage
- Detect overspending

## Daily Log
- Record daily financial activities
- Generate daily summaries

## Asset Management
- Manage assets
- Calculate net worth

## Debt Management
- Track debts
- Manage repayments

## Automation Engine
- Execute scheduled tasks
- Generate recurring records

## Reporting
- Produce financial reports
- Export report data

## Analytics
- Generate financial insights
- Analyze spending patterns

## Archive
- Preserve historical records
- Support data recovery
---

# Module Interaction

Presentation Layer
↓
Application Layer
↓
Financial Engine
├── Budget Engine
├── Asset Management
├── Debt Management
├── Automation Engine
└── Reporting
↓
Data Layer (PostgreSQL)
---

# Database Architecture

Database: PostgreSQL

ORM: Prisma

Core Domains:

- Accounts
- Transactions
- Budgets
- Assets
- Debts
- Categories
- Automation Jobs
- Reports
- Audit Logs

Principles:

- Normalize data where practical.
- Preserve historical records.
- Use foreign keys to maintain integrity.
- Soft delete financial records instead of permanent deletion where appropriate.
