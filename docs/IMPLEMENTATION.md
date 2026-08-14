# FinMang OS — Phase 6 Implementation

## Scope

This implementation targets the approved MVP specification. The MVP boundary includes Accounts, Categories, Transactions, Balance, the defined financial calculations, internal audit logging, and the CLI workflows. Budgets, assets, debts, automation, reporting/analytics, authentication, and the React frontend remain outside this MVP implementation unless separately approved by the authoritative roadmap/specifications.

## Backend

- Python
- FastAPI
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- Pydantic

## Implemented API

- `GET /health`
- `GET/POST /api/v1/accounts`
- `GET/PATCH/DELETE /api/v1/accounts/{account_id}`
- `GET/POST /api/v1/categories`
- `GET/PATCH/DELETE /api/v1/categories/{category_id}`
- `GET/POST /api/v1/transactions`
- `GET/PATCH/DELETE /api/v1/transactions/{transaction_id}` (delete intentionally rejected in MVP)
- `GET /api/v1/accounts/{account_id}/balance`
- `GET /api/v1/balance`

## Financial controls

- Decimal monetary values
- Positive transaction amounts
- No future transaction dates
- Transaction/category type matching
- Inactive accounts reject new transactions
- System categories cannot be modified/deleted
- Categories referenced by transactions cannot be deleted
- Transaction deletion is rejected
- Audit records are written for financial mutations
- Balances are derived from transactions rather than trusted from a mutable cached value

## Verification

The repository contains API tests covering health, account/category/transaction flow, balance calculation, invalid amounts, future dates, category mismatch, and inactive-account rejection. CI runs the backend test suite on pushes and pull requests.
