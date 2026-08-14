# FinMang OS Database Schema

Version: 3.0
Status: Official (MVP Locked)

---

## Purpose
This document defines the database tables, columns, keys, and relationships for the MVP. Matches Domain Model in ARCHITECTURE.md.

---

## Tables (MVP)

### 1. accounts
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `name` | VARCHAR(100) | NOT NULL | Display name |
| `type` | ENUM | NOT NULL | `CHECKING`, `SAVINGS`, `CREDIT`, `CASH`, `E_WALLET` |
| `balance` | DECIMAL(15,2) | DEFAULT 0.00 | Current total balance |
| `currency` | VARCHAR(3) | NOT NULL | ISO code (MYR, USD) |
| `institution` | VARCHAR(100) | | Bank/provider name |
| `is_active` | BOOLEAN | DEFAULT TRUE | Soft delete flag |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

---

### 2. categories
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `name` | VARCHAR(50) | NOT NULL | e.g., "Groceries" |
| `type` | ENUM | NOT NULL | `INCOME` or `EXPENSE` |
| `parent_id` | UUID | FOREIGN KEY (references `categories.id`) | Nullable for sub-categories |
| `color` | VARCHAR(7) | | Hex color code |
| `is_system` | BOOLEAN | DEFAULT FALSE | Prevents deletion of default categories |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

---

### 3. transactions
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `account_id` | UUID | FOREIGN KEY (references `accounts.id`) | Which account |
| `category_id` | UUID | FOREIGN KEY (references `categories.id`) | Which category |
| `amount` | DECIMAL(15,2) | NOT NULL | Monetary value |
| `type` | ENUM | NOT NULL | `INCOME`, `EXPENSE`, or `TRANSFER` |
| `description` | VARCHAR(255) | | Optional user note |
| `transaction_date` | DATE | NOT NULL | When it occurred |
| `is_reconciled` | BOOLEAN | DEFAULT FALSE | Matches bank statement |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

---

### 4. budgets
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `category_id` | UUID | FOREIGN KEY (references `categories.id`) | Must be EXPENSE type |
| `amount` | DECIMAL(15,2) | NOT NULL | Allocated limit |
| `period` | ENUM | NOT NULL | `MONTHLY` or `YEARLY` |
| `start_date` | DATE | NOT NULL | Cycle start |
| `end_date` | DATE | NOT NULL | Cycle end |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

---

### 5. assets
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `name` | VARCHAR(100) | NOT NULL | Asset name |
| `type` | ENUM | NOT NULL | `PROPERTY`, `VEHICLE`, `INVESTMENT`, `VALUABLE` |
| `purchase_price` | DECIMAL(15,2) | NOT NULL | Original cost |
| `current_value` | DECIMAL(15,2) | NOT NULL | Estimated market value |
| `purchase_date` | DATE | NOT NULL | Date acquired |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

---

### 6. debts
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `name` | VARCHAR(100) | NOT NULL | Debt name |
| `type` | ENUM | NOT NULL | `LOAN`, `MORTGAGE`, `CREDIT_CARD`, `PERSONAL` |
| `principal` | DECIMAL(15,2) | NOT NULL | Original amount borrowed |
| `remaining_balance` | DECIMAL(15,2) | NOT NULL | Current outstanding amount |
| `interest_rate` | DECIMAL(5,2) | NOT NULL | Annual interest rate (%) |
| `due_date` | DATE | NOT NULL | Next payment due date |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

---

### 7. automation_jobs
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `name` | VARCHAR(100) | NOT NULL | Job display name |
| `trigger_type` | ENUM | NOT NULL | `SCHEDULE` or `WEBHOOK` |
| `schedule_cron` | VARCHAR(100) | | Cron expression (if SCHEDULE) |
| `action_type` | ENUM | NOT NULL | `CREATE_TRANSACTION`, `GENERATE_REPORT`, `SEND_ALERT` |
| `config` | JSON | NOT NULL | Payload for the action |
| `is_active` | BOOLEAN | DEFAULT TRUE | Enable/disable |
| `last_run` | TIMESTAMP | | Last execution timestamp |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

---

## Relationships (MVP)
- **accounts** (1) → (∞) **transactions**
- **categories** (1) → (∞) **transactions**
- **categories** (1) → (∞) **budgets** (optional)
- **transactions** do NOT link to assets/debts in MVP (Phase 2+).

---

## Indexes (Recommended)
- `transactions.account_id` (for fast account lookups)
- `transactions.category_id` (for category reports)
- `transactions.transaction_date` (for date range queries)
- `categories.parent_id` (for sub-category queries)

---

## Notes
- All UUIDs generated by application (Python `uuid.uuid4()`, mapped via SQLAlchemy).
- Soft delete = `is_active = false`. Do not physically delete records.
- ENUMs are PostgreSQL-native, defined via SQLAlchemy `Enum` types.
- JSON config for automation allows flexible future actions.
- Schema migrations managed through Alembic (see ADR-002).
