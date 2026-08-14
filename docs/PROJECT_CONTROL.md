# FinMang OS — Project Control

## Operating Mode

FinMang OS is being executed block-by-block under controlled GitHub changes.

## Source-of-Truth Baseline

- `main`: legacy repository baseline.
- `finmang-os-updated.zip`: Claude-remediated repository baseline supplied to the project on 2026-08-14.
- `cto/block-0-reconciliation`: controlled working branch for reconciliation and subsequent implementation.

## Block 0 — Source-of-Truth Reconciliation

Status: IN PROGRESS

Objectives:

1. Compare the current GitHub repository with the Claude-remediated repository.
2. Preserve existing Git history.
3. Establish the remediated documentation/specification state as the implementation baseline.
4. Do not merge to `main` until reconciliation and verification are complete.

Initial findings:

- GitHub `main` is behind the remediated repository.
- The remediated repository introduces `docs/ADR/ADR-002-Backend-Stack-Revision.md`.
- The remediated repository expands `docs/API_SPEC.md` and `docs/BUSINESS_LOGIC.md`.
- The remediated repository updates architecture, database, MVP, roadmap/state/task documentation, repository hygiene, and Notion status documentation.
- `docs/ROADMAP.md` remains the authoritative roadmap.
- Backend/database tooling is locked to Python + FastAPI + SQLAlchemy + Alembic.

## Execution Rule

A block is considered complete only when its implementation, tests/verification, documentation, and Git state have been checked.

## Next Gate

Complete the file-level reconciliation, then proceed to Block 1 — Repository Reconciliation and implementation preparation.
