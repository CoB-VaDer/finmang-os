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
---

# API Architecture

Style: REST API

Base Path:

/api/v1

Core Endpoints:

- /accounts
- /transactions
- /budgets
- /assets
- /debts
- /categories
- /reports
- /analytics
- /automation

Principles:

- Stateless requests
- JSON request and response bodies
- Consistent error responses
- API versioning from the beginning
- Authentication required for protected endpoints
---

# Frontend Architecture

Framework: React

Language: TypeScript

Build Tool: Vite

Principles:

- Component-based architecture
- Feature-first organization
- Reusable UI components
- Client-side routing
- Responsive design
- Accessibility by default
- API communication through a dedicated service layer
---

# Project Structure

```
finmang-os/
├── docs/
├── database/
├── automation/
├── assets/
├── archive/
├── backend/
├── frontend/
├── scripts/
├── tests/
├── .github/
├── README.md
└── .gitignore
```

Each top-level directory has a single, well-defined responsibility.

---

# Security Architecture

Principles:

- Authentication required for protected resources.
- Authorization based on user roles and permissions.
- Passwords stored using secure hashing.
- HTTPS for all production traffic.
- Input validation on every API endpoint.
- Audit logging for sensitive financial operations.

---

# Deployment Architecture

Environment:

- Development
- Staging
- Production

Deployment Principles:

- Automated deployments
- Environment-based configuration
- Database migrations managed through Prisma
- Backup strategy for production data
- Monitoring and logging enabled

---

# System Context

The overall system architecture follows this flow:

```
User
    ↓
Frontend (React)
    ↓
REST API
    ↓
Application Layer
    ↓
Domain Layer
    ↓
Infrastructure Layer
    ↓
PostgreSQL Database
```

Each layer has a single responsibility and communicates only with adjacent layers to maintain loose coupling and high cohesion.

---

---

# Module Ownership

Each business domain has a single owning module.

| Domain | Owner Module |
|----------|--------------|
| Accounts | Financial Engine |
| Transactions | Financial Engine |
| Budgets | Budget Engine |
| Assets | Asset Management |
| Debts | Debt Management |
| Daily Records | Daily Log |
| Automation Jobs | Automation Engine |
| Reports | Reporting |
| Analytics Data | Analytics |
| Archived Data | Archive |

Only the owning module is responsible for creating, updating, and deleting its domain data. Other modules must interact through the Application Layer rather than accessing another module's data directly.

---
---

# Module Dependency Rules

To maintain a clean architecture, modules must follow these rules:

- Modules communicate through the Application Layer.
- Modules do not access another module's database tables directly.
- Business logic belongs only in the owning module.
- Reporting and Analytics are read-only consumers of business data.
- The Automation Engine orchestrates workflows but does not own business data.
- Shared functionality belongs in common services, not business modules.

These rules ensure loose coupling, maintainability, and scalability.

---
---

# Cross-Cutting Concerns

The following concerns apply across the entire system and are not owned by any single module:

- Authentication
- Authorization
- Configuration Management
- Logging
- Error Handling
- Input Validation
- Audit Logging
- Performance Monitoring

These concerns are implemented as shared infrastructure and must remain independent of business modules.

---
# Domain Model (Business Objects)

*This section defines the core business entities, their attributes, data types, and relationships. This is the single source of truth for what data the system manages for the MVP.*

---

## 1. Account
Represents a financial account (bank, cash, e-wallet).

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID (PK) | Unique identifier |
| `name` | String(100) | Display name (e.g., "Maybank Current") |
| `type` | Enum | `CHECKING`, `SAVINGS`, `CREDIT`, `CASH`, `E_WALLET` |
| `balance` | Decimal(15,2) | Current total balance |
| `currency` | String(3) | ISO currency code (e.g., `MYR`, `USD`) |
| `institution` | String(100) | Bank or provider name |
| `is_active` | Boolean | Soft-delete flag (default: `true`) |
| `created_at` | Timestamp | Creation timestamp |
| `updated_at` | Timestamp | Last update timestamp |

**Relationships:** An Account has many **Transactions**.

---

## 2. Category
Categorizes transactions for reporting and budgeting.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID (PK) | Unique identifier |
| `name` | String(50) | e.g., "Groceries", "Salary" |
| `type` | Enum | `INCOME` or `EXPENSE` |
| `parent_id` | UUID (FK) | Nullable. Self-referencing for sub-categories (e.g., "Food" → "Groceries") |
| `color` | String(7) | Hex color code for UI |
| `is_system` | Boolean | True for default system categories (prevents deletion) |
| `created_at` | Timestamp | Creation timestamp |

**Relationships:** A Category has many **Transactions**. A Category may have many sub-Categories.

---

## 3. Transaction
Records a single inflow or outflow of money.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID (PK) | Unique identifier |
| `account_id` | UUID (FK) | References **Account** |
| `category_id` | UUID (FK) | References **Category** |
| `amount` | Decimal(15,2) | Monetary value |
| `type` | Enum | `INCOME`, `EXPENSE`, or `TRANSFER` |
| `description` | String(255) | Optional user note |
| `transaction_date` | Date | Date the transaction occurred |
| `is_reconciled` | Boolean | Matches bank statement (default: `false`) |
| `created_at` | Timestamp | Creation timestamp |
| `updated_at` | Timestamp | Last update timestamp |

**Relationships:** Belongs to an **Account** and a **Category**.

---

## 4. Budget
Allocates a spending limit to a specific Category over a period.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID (PK) | Unique identifier |
| `category_id` | UUID (FK) | References **Category** (must be EXPENSE type) |
| `amount` | Decimal(15,2) | Allocated budget limit |
| `period` | Enum | `MONTHLY`, `YEARLY` |
| `start_date` | Date | Start of the budget cycle |
| `end_date` | Date | End of the budget cycle |
| `created_at` | Timestamp | Creation timestamp |
| `updated_at` | Timestamp | Last update timestamp |

**Relationships:** Belongs to a **Category**.

---

## 5. Asset
Represents items of value owned (Property, Vehicles, Investments).

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID (PK) | Unique identifier |
| `name` | String(100) | e.g., "Toyota Camry" |
| `type` | Enum | `PROPERTY`, `VEHICLE`, `INVESTMENT`, `VALUABLE` |
| `purchase_price` | Decimal(15,2) | Original cost |
| `current_value` | Decimal(15,2) | Estimated current market value |
| `purchase_date` | Date | Date acquired |
| `created_at` | Timestamp | Creation timestamp |
| `updated_at` | Timestamp | Last update timestamp |

---

## 6. Debt (Liability)
Represents money owed (Loans, Mortgages, Credit Card balances).

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID (PK) | Unique identifier |
| `name` | String(100) | e.g., "Housing Loan" |
| `type` | Enum | `LOAN`, `MORTGAGE`, `CREDIT_CARD`, `PERSONAL` |
| `principal` | Decimal(15,2) | Original amount borrowed |
| `remaining_balance` | Decimal(15,2) | Current outstanding amount |
| `interest_rate` | Decimal(5,2) | Annual interest rate percentage |
| `due_date` | Date | Next payment due date |
| `created_at` | Timestamp | Creation timestamp |
| `updated_at` | Timestamp | Last update timestamp |

---

## 7. Automation Job
Defines a scheduled or event-driven task for n8n or internal cron.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID (PK) | Unique identifier |
| `name` | String(100) | e.g., "Monthly Salary Entry" |
| `trigger_type` | Enum | `SCHEDULE`, `WEBHOOK` |
| `schedule_cron` | String | Cron expression (if `trigger_type` is `SCHEDULE`) |
| `action_type` | Enum | `CREATE_TRANSACTION`, `GENERATE_REPORT`, `SEND_ALERT` |
| `config` | JSON | Payload/configuration for the action |
| `is_active` | Boolean | Enable/disable the job |
| `last_run` | Timestamp | Last execution timestamp |
| `created_at` | Timestamp | Creation timestamp |
| `updated_at` | Timestamp | Last update timestamp |

---

## Entity Relationship Summary (MVP)
- **Account** (1) ─── (∞) **Transaction**
- **Category** (1) ─── (∞) **Transaction**
- **Category** (1) ─── (∞) **Budget** (optional for MVP)
- **Transaction** does NOT directly link to Asset/Debt in MVP (reserved for Phase 2).
