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

Balance is never stored as an editable field — it is always derived from transactions, so it can never drift from the transaction history (Amanah: Traceable).

```
account_balance = SUM(amount WHERE type = 'INCOME' AND account_id = X)
                 - SUM(amount WHERE type = 'EXPENSE' AND account_id = X)
```

`TRANSFER` transactions net to zero across the two accounts involved and do not affect total balance across all accounts.

### Total Balance (all accounts)

```
total_balance = SUM(account_balance) for all accounts WHERE is_active = true
```

This is the value returned by the MVP "View Balance" workflow (see `WORKFLOWS.md`).

### Category Spending Total (period)

```
category_spent = SUM(amount WHERE category_id = X
                        AND type = 'EXPENSE'
                        AND transaction_date BETWEEN period_start AND period_end)
```

### Budget Usage Percentage (Phase 2 — Budget entity, documented here for completeness since it depends on the Category Spending formula above)

```
budget_usage_pct = (category_spent / budget.amount) * 100
```

A budget is considered exceeded when `budget_usage_pct > 100`. This triggers the overspending detection described in `docs/ARCHITECTURE.md`'s Budget Engine module.

### Net Worth (Phase 2 — Asset/Debt entities, documented here for completeness)

```
net_worth = SUM(asset.current_value) - SUM(debt.remaining_balance)
```

### Debt Remaining Balance (Phase 2)

`remaining_balance` is tracked directly on the Debt record (see `database/DATABASE_SCHEMA.md`) and decremented by recorded repayments; it is not derived from transactions in the MVP data model, since Transactions do not link to Debts until Phase 2 (see Entity Relationship Summary in `docs/ARCHITECTURE.md`).

---

## Rounding and Precision

All monetary values use `DECIMAL(15,2)` (see `database/DATABASE_SCHEMA.md`) — never floating-point types — to avoid rounding errors in financial calculations (Amanah: Measurable). All calculations above are performed in decimal arithmetic, and results are rounded to 2 decimal places using standard half-up rounding.
