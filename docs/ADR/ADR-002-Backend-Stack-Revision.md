# ADR-002: Backend Stack Revision (Supersedes ADR-001 Backend Decision)

## Status

Accepted

## Context

ADR-001 (status: Proposed, never formally accepted) specified a Node.js + Express + TypeScript backend with Prisma ORM. In practice, backend implementation work began against a different stack: Python with FastAPI, SQLAlchemy, and psycopg2 (see `backend/requirements.txt`). `docs/MVP.md` also listed the backend language as "TBD" between Python and Node, meaning no single document actually reflected an approved, current decision.

Per the Constitution, an existing ADR must not be silently overridden — a decision change requires a new ADR that explicitly supersedes the old one. This ADR performs that function and resolves the inconsistency identified in the FinMang OS Documentation Audit (Finding 1, August 2026).

## Decision

The backend stack is:

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.x
- **Database driver:** psycopg2 (PostgreSQL)
- **Validation:** Pydantic v2
- **Migrations:** Alembic (replaces Prisma Migrate)
- **Backend testing:** pytest

All other technology decisions from ADR-001 remain unchanged and in effect:

- **Frontend:** React, TypeScript, Vite (Phase 2+, out of scope for MVP per `docs/MVP.md`)
- **Database:** PostgreSQL
- **Authentication:** JWT
- **Frontend testing:** Vitest, Playwright (Phase 2+)
- **Version control:** Git, GitHub
- **Editor:** VS Code

## Rationale

- Backend implementation had already started against FastAPI/SQLAlchemy (`backend/requirements.txt`); reversing to Node would discard working code for no functional benefit.
- FastAPI's built-in request/response validation (Pydantic) maps directly onto the validation rules already defined in `BUSINESS_LOGIC.md`.
- FastAPI auto-generates OpenAPI documentation, giving a head start on keeping `API_SPEC.md` accurate.
- SQLAlchemy is a mature ORM well suited to precise decimal handling required for financial data.
- ADR-001's backend decision was never formally accepted, so there is no approved decision being reversed — only an unapproved proposal being replaced with the stack already in use.

## Consequences

- `docs/ARCHITECTURE.md` must be updated to reference SQLAlchemy/Alembic instead of Prisma in the Database Architecture and Deployment Architecture sections.
- `docs/MVP.md` must be updated to state the backend decision as final, not "TBD."
- `.gitignore` must be updated to include Python-specific ignore patterns (see Finding 7, repo hygiene block).
- Frontend stack (React/TypeScript/Vite) is unaffected and remains deferred to Phase 2+.

---

Version: 1.0
Status: Accepted
Supersedes: ADR-001 (backend/database-tooling portion only; frontend/auth/VCS decisions in ADR-001 remain in effect)
