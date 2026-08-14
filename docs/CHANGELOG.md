# Changelog

All notable changes to this project will be documented in this file.

---

## [0.2.0] - 2026-08-14

### Added
- **docs/ADR/ADR-002-Backend-Stack-Revision.md** — Formal ADR locking in Python/FastAPI/SQLAlchemy/Alembic as the backend stack, superseding the never-accepted Node.js/Prisma decision in ADR-001.

### Changed
- **docs/ADR/ADR-001-Technology-Stack.md** — Status updated to "Superseded (backend/database-tooling only)"; frontend/auth/VCS decisions remain in effect.
- **docs/ARCHITECTURE.md** — Database and Deployment Architecture sections updated to reference SQLAlchemy/Alembic instead of Prisma.
- **database/DATABASE_SCHEMA.md** — Notes section updated to reference SQLAlchemy/Alembic instead of Prisma.
- **docs/MVP.md** — Backend technology changed from "TBD" to decided (Python/FastAPI), referencing ADR-002.
- **docs/STATE.md** — Current Phase label corrected from "Phase 4 — Backend Foundation" to "Phase 5 — Project Management" to align with docs/ROADMAP.md's phase numbering; version bumped to 2.1.
- **README.md** — Removed duplicate, stale roadmap and status section; now points to docs/ROADMAP.md and docs/STATE.md as the single sources of truth.
- **meeting/PROJECT_ROADMAP.md** — Marked as superseded/historical; docs/ROADMAP.md is now the sole authoritative roadmap.
- **notion/README.md** — Added to clarify the folder's status (reserved, not yet started) instead of an unexplained empty directory.

### Fixed
- **docs/CONSTITUTION.md** — Removed a stray "git add ." string accidentally embedded in Rule 7 of Project Governance.
- **docs/API_SPEC.md** — Actually written. Was previously marked complete in [0.1.0] but contained no endpoint definitions. Now specifies all MVP endpoints (Accounts, Categories, Transactions, Balance) with request/response formats and error codes, cross-referenced to BUSINESS_LOGIC.md validation rules.
- **docs/BUSINESS_LOGIC.md** — Calculation Formulas section completed. Was previously marked complete in [0.1.0] but cut off after the section heading with no formulas. Now includes Account Balance, Total Balance, Category Spending, Budget Usage %, Net Worth, and Debt Remaining Balance formulas, plus a Rounding and Precision note.
- **backend/requirements.txt** — Converted from UTF-16LE (with BOM, CRLF line endings) to plain UTF-8/LF, matching every other file in the repo. Added `alembic` as a dependency per ADR-002.
- **.gitignore** — Added a full set of Python ignore patterns (`__pycache__/`, `*.pyc`, `.venv/`, `.pytest_cache/`, etc.), which were entirely missing despite Python being the actual backend language in use.

### Note
This entry documents a documentation-integrity audit and cleanup pass. It does not rewrite the [0.1.0] history below (per Constitution rules on not rewriting prior records) — it corrects the record going forward.

---

## [0.1.0] - 2026-07-06

### Added

#### Phase 4: Engineering Specification (Complete)
- **Domain Model** — Added to ARCHITECTURE.md (7 entities: Account, Category, Transaction, Budget, Asset, Debt, Automation Job)
- **WORKFLOWS.md** — Created with MVP workflows (Add Income, Add Expense, View Balance, List Transactions)
- **DATABASE_SCHEMA.md** — Expanded with 7 tables matching Domain Model
- **BUSINESS_LOGIC.md** — Expanded with validation rules, calculation formulas, Islamic finance (Amanah) principles
- **API_SPEC.md** — Created with REST endpoints for MVP (Accounts, Categories, Transactions, Budgets)
- **MVP.md** — Created with MVP scope locked

### Changed
- None

### Fixed
- None

### Removed
- Mission table removed from DATABASE_SCHEMA.md (not needed for MVP)

---

## [0.0.1] - 2026-07-05

### Added
- Initial repository structure
- Documentation files (ARCHITECTURE.md, CONSTITUTION.md, MISSION.md, VISION.md, etc.)
- Project Charter
- Constitution (Amanah principles)

---

Version: 1.0
Status: Official
