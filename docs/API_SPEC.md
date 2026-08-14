# FinMang OS - API Specification

Version: 1.1
Status: Official (MVP Locked)

---

## Purpose

This document defines the REST API endpoints, request/response formats, and error codes for the MVP.

Note: The MVP itself is CLI-only (see `docs/MVP.md`) — this API layer is the interface the CLI (and any future frontend) calls internally. It is documented now so the backend implementation (Phase 6) has a contract to build against.

---

## Base URL

```
/api/v1
```

Per `docs/ARCHITECTURE.md`: stateless requests, JSON request/response bodies, consistent error responses, versioned from the start. Authentication (JWT) is out of scope for the MVP per `docs/MVP.md` and is not required on these endpoints yet.

---

## Scope

This specification covers only the MVP data models: **Accounts**, **Categories**, **Transactions**. Budgets, Assets, Debts, Automation Jobs, Reports, and Analytics endpoints are reserved for Phase 2+ and are intentionally not defined here (see `docs/MVP.md` exclusions).

---

## Common Response Envelope

### Success

```json
{
  "data": { },
  "error": null
}
```

### Error

```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Amount must be greater than zero."
  }
}
```

Error messages match the validation rules defined in `docs/BUSINESS_LOGIC.md` exactly, so the API and the business rules document never drift apart.

---

## Endpoints

### Accounts

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/accounts` | List all accounts (active by default; `?include_inactive=true` to include soft-deleted). |
| `POST` | `/accounts` | Create a new account. |
| `GET` | `/accounts/{id}` | Retrieve a single account. |
| `PATCH` | `/accounts/{id}` | Update account fields (name, institution, currency). Balance is never set directly — see Business Rule below. |
| `DELETE` | `/accounts/{id}` | Soft-delete (sets `is_active = false`). No hard deletes, per `docs/BUSINESS_LOGIC.md`. |

**Create request body:**

```json
{
  "name": "Maybank Current",
  "type": "CHECKING",
  "currency": "MYR",
  "institution": "Maybank"
}
```

**Business rule:** `balance` is a derived/computed field (see Calculation Formulas in `docs/BUSINESS_LOGIC.md`) and cannot be set directly via the API. It always reflects the sum of the account's transactions.

**Errors:** `404 ACCOUNT_NOT_FOUND` — "Account not found." · `409 ACCOUNT_INACTIVE` — "Account is inactive."

---

### Categories

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/categories` | List all categories. `?type=INCOME|EXPENSE` to filter. |
| `POST` | `/categories` | Create a new category. |
| `GET` | `/categories/{id}` | Retrieve a single category. |
| `PATCH` | `/categories/{id}` | Update a category (name, color, parent_id). System categories (`is_system = true`) cannot be renamed or deleted. |
| `DELETE` | `/categories/{id}` | Delete a category. Rejected if `is_system = true` or if transactions reference it. |

**Create request body:**

```json
{
  "name": "Groceries",
  "type": "EXPENSE",
  "parent_id": null,
  "color": "#4CAF50"
}
```

**Errors:** `404 CATEGORY_NOT_FOUND` — "Category not found." · `409 CATEGORY_IN_USE` — "Category cannot be deleted while referenced by transactions." · `409 SYSTEM_CATEGORY` — "System categories cannot be modified or deleted."

---

### Transactions

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/transactions` | List transactions. Supports `?account_id=`, `?category_id=`, `?type=`, `?date_from=`, `?date_to=` filters and pagination (`?page=`, `?page_size=`). |
| `POST` | `/transactions` | Create a transaction (income, expense, or transfer). |
| `GET` | `/transactions/{id}` | Retrieve a single transaction. |
| `PATCH` | `/transactions/{id}` | Update a transaction's mutable fields (description, category, is_reconciled). Amount/account/type are immutable after creation — correct mistakes by creating a reversing entry, per the Amanah traceability principle in `docs/BUSINESS_LOGIC.md`. |
| `DELETE` | `/transactions/{id}` | Not supported in MVP. No deletion — see Workflow Rules in `WORKFLOWS.md` ("No deletion in MVP, soft delete only"). Returns `405 METHOD_NOT_ALLOWED`. |

**Create request body:**

```json
{
  "account_id": "uuid",
  "category_id": "uuid",
  "amount": 150.00,
  "type": "EXPENSE",
  "description": "Weekly groceries",
  "transaction_date": "2026-08-14"
}
```

**Validation errors** (from `docs/BUSINESS_LOGIC.md`, reproduced here so the API contract and business rules never diverge):

| HTTP Status | Code | Message |
| :--- | :--- | :--- |
| 422 | `INVALID_AMOUNT` | "Amount must be greater than zero." |
| 422 | `FUTURE_DATE` | "Date cannot be in the future." |
| 404 | `CATEGORY_NOT_FOUND` | "Category not found." |
| 422 | `CATEGORY_TYPE_MISMATCH` | "Category type does not match transaction type." |
| 404 | `ACCOUNT_NOT_FOUND` | "Account not found." |
| 409 | `ACCOUNT_INACTIVE` | "Account is inactive." |

---

### Balance

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/accounts/{id}/balance` | Returns the computed current balance for one account. |
| `GET` | `/balance` | Returns the computed total balance across all active accounts (the MVP "View Balance" workflow). |

**Response:**

```json
{
  "data": {
    "total_income": 5000.00,
    "total_expense": 3200.00,
    "balance": 1800.00
  },
  "error": null
}
```

Calculation matches the Account Balance formula in `docs/BUSINESS_LOGIC.md`.

---

## Standard Error Codes

| HTTP Status | Meaning |
| :--- | :--- |
| 400 | Malformed request body |
| 404 | Resource not found |
| 405 | Method not allowed (e.g., deleting a transaction) |
| 409 | Conflict with current resource state (inactive account, system category, etc.) |
| 422 | Validation failure (see per-endpoint tables above) |
| 500 | Internal server error |

---

## Out of Scope for MVP

The following endpoint groups are referenced in `docs/ARCHITECTURE.md` as part of the full system but are explicitly excluded from the MVP per `docs/MVP.md`, and are not specified here: `/budgets`, `/assets`, `/debts`, `/reports`, `/analytics`, `/automation`. These will be specified in their own ADR/spec update when their implementation phase begins.
