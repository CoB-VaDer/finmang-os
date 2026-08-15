# ADR-002: Backend Stack Revision

- **Status:** Accepted
- **Date:** 2026-08-16
- **Supersedes:** The backend technology choice recorded as planned/TBD in `docs/MVP.md` and the original backend direction in ADR-001.

## Context

The original project documentation established PostgreSQL as the MVP database and left the backend as `Python (FastAPI) or Node.js (TBD)`. ADR-001 records the earlier Node.js/Express/TypeScript/Prisma direction. During MVP implementation, the project adopted a Python/FastAPI backend with SQLAlchemy and Alembic.

The implemented stack is now the source of truth for the Phase 6 MVP and deployment foundation. The repository contains the corresponding FastAPI application, SQLAlchemy models/services, Alembic migrations, PostgreSQL integration, Dockerfile, and tests.

## Decision

FinMang-OS will use the following backend stack for the current MVP and Phase 6/7 deployment foundation:

- **Language:** Python
- **API framework:** FastAPI
- **ORM/database toolkit:** SQLAlchemy 2.x
- **Database migration tool:** Alembic
- **Database:** PostgreSQL
- **Container/runtime:** Docker

This decision does not expand the MVP feature scope. It records the implementation choice needed to make the repository's architecture and deployment documentation consistent with the code already merged into `main`.

## Consequences

### Positive

- The documented architecture matches the implemented backend.
- FastAPI provides the current HTTP API and `/health` endpoint.
- SQLAlchemy and Alembic provide the current persistence and migration layers.
- PostgreSQL remains the MVP persistence requirement.
- Docker provides the deployment packaging used by the staging plan.

### Trade-offs

- The repository no longer follows the Node.js/Express/TypeScript/Prisma backend direction from ADR-001.
- Existing documentation that described the backend as undecided must be interpreted in light of this accepted decision.
- PostgreSQL-backed staging validation is still required before deployment can be considered successful.

## Non-goals

This ADR does not authorize authentication, frontend UI, analytics, automation, Zakat calculations, or other Phase 2+ functionality excluded by the MVP definition.

## Validation requirement

The stack decision is documented and implemented, but deployment readiness is not implied by this ADR. Live staging must still verify container startup, Alembic migration execution against PostgreSQL, API smoke tests, persistence, and backup/restore according to `docs/DEPLOYMENT_STATUS.md`.
