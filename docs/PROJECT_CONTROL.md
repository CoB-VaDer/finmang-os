# FinMang OS — Project Control

## Operating model

FinMang OS is driven block-by-block under CTO/COO/PMO control. Each block must be implemented, verified, documented, and reflected in Git history before it is considered complete.

## Source of truth

- The existing GitHub `main` branch is the legacy repository baseline.
- The Claude-remediated `finmang-os-updated.zip` supplied on 2026-08-14 is the remediation baseline for documentation/specification reconciliation.
- Approved implementation work is performed in controlled feature branches and promoted through pull requests.

## Current execution sequence

1. Block 0 — Source-of-truth reconciliation
2. Block 1 — Repository reconciliation
3. Block 2 — Architecture lock
4. Block 3 — Database implementation
5. Block 4 — Financial business logic
6. Block 5 — API implementation
7. Block 6 — MVP application/CLI
8. Block 7 — Security
9. Block 8 — QA and acceptance
10. Block 9 — Documentation synchronization
11. Block 10 — Production release

## Git rules

- `main` is not modified directly for project work.
- Work is performed on controlled branches.
- Draft PRs are used while a block is in progress.
- A block may be merged only after its stated exit criteria are verified.
- Production readiness requires implementation, tests, documentation, and release verification.
