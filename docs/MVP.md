# FinMang OS - MVP Definition

Version: 1.0
Status: Official (Locked)

---

## MVP Scope (Phase 1)

**What is included:**

### Core Features
- Add Income
- Add Expense
- View Balance
- List Transactions
- Basic Categories (Income/Expense)

### Data Models (MVP Only)
- Accounts
- Categories
- Transactions

### Technology (Decided — see ADR-002)
- Backend: Python (FastAPI)
- Database: PostgreSQL (via SQLAlchemy + Alembic)
- Frontend: CLI only (no UI for MVP)

---

## What is EXCLUDED (Phase 2+)
- Budget tracking
- Asset management
- Debt management
- Automation (n8n)
- Reporting/Analytics
- Authentication
- Frontend UI (React)
- Zakat calculations
- API authentication

---

## MVP Success Criteria
1. User can add income via CLI.
2. User can add expense via CLI.
3. User can view current balance.
4. User can list all transactions.
5. Data persists in PostgreSQL.
6. All code is in version control.

---

## MVP Timeline
- Documentation Phase: COMPLETE
- Implementation: Start after MVP.md approval

---

Version: 1.0
Status: Official (Locked)
