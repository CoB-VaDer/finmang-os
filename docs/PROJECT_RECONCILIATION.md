# FinMang OS — Source-of-Truth Reconciliation

**Date:** 2026-08-14  
**Working branch:** `cto/block-0-reconciliation`  
**Legacy baseline:** `main`  
**Remediated baseline:** `finmang-os-updated.zip` supplied after Claude audit

## Decision

The Claude-remediated repository is the candidate specification baseline for FinMang OS. The legacy `main` branch is preserved unchanged until reconciliation is verified and approved for merge.

## Evidence

The remediation summary states that all 9 audit findings were resolved across four remediation blocks and that `finmang-os-updated.zip` is the updated repository ready for Phase 6 implementation.

## Candidate changed/new files

- `.gitignore`
- `README.md`
- `backend/requirements.txt`
- `database/DATABASE_SCHEMA.md`
- `docs/ADR/ADR-001-Technology-Stack.md`
- `docs/ADR/ADR-002-Backend-Stack-Revision.md` (new)
- `docs/API_SPEC.md`
- `docs/ARCHITECTURE.md`
- `docs/BUSINESS_LOGIC.md`
- `docs/CHANGELOG.md`
- `docs/CONSTITUTION.md`
- `docs/MVP.md`
- `docs/ROADMAP.md`
- `docs/STATE.md`
- `docs/TASKS.md`
- `meeting/PROJECT_ROADMAP.md`
- `notion/README.md` (new)

## Candidate remediated file hashes

SHA-1 values calculated from the supplied ZIP:

| File | SHA-1 |
|---|---|
| `.gitignore` | `b0895a1eb60b6ef4a7134b3d4213da45e7287cf3` |
| `README.md` | `5e4e697713a0c7aaffe085b76cb3e8619e5ea52a` |
| `backend/requirements.txt` | `a326da97a729e6f7dfaf34913d09c0d71a082c26` |
| `database/DATABASE_SCHEMA.md` | `d13b3437f5b58b371c5a986f89dd1df6ff5a2c54` |
| `docs/API_SPEC.md` | `905810e475bbe272b5812ca950bd3df29dded787` |
| `docs/ARCHITECTURE.md` | `f6634b7f9286e5fde2d073e3bff8e861c07a1564` |
| `docs/BUSINESS_LOGIC.md` | `9f79d18b12a00b44c7b6d1b2b01e30689b5863d4` |
| `docs/CHANGELOG.md` | `d2cfde5f418e6fa7893ffeafd888beb501a5ba3d` |
| `docs/CONSTITUTION.md` | `3fec155c4dfc14bff6da827816c0cf8b64fbb5f9` |
| `docs/MVP.md` | `ed00479d8b65c2d23e28f7661a30a95eb520958e` |
| `docs/ROADMAP.md` | `b6b8b5ec93d15483eda7d5703b32eee1840b8e9a` |
| `docs/STATE.md` | `dfb4706b3c2c7e76ea82524b1c23d2df03fd67f2` |
| `docs/TASKS.md` | `d4ab40eb04c744d108310f8f3d0d54dc49b126b9` |
| `docs/ADR/ADR-001-Technology-Stack.md` | `383a58f1d1c5543e47d4f7631088169ee353b517` |
| `docs/ADR/ADR-002-Backend-Stack-Revision.md` | `1ecb415d1cc77a64124f5fcf0c2d19bd7b46a335` |
| `meeting/PROJECT_ROADMAP.md` | `c7692208531ca3d640240c1a6a7de1fd31016f19` |
| `notion/README.md` | `c1deb28a2a897b5cf6bb0e66cdd113ad363469cc` |

## Control rule

No merge into `main` until the candidate remediated files have been transferred and verified. Phase 6 implementation begins only after this baseline is established.

## Exit criteria

- [x] GitHub access verified
- [x] Working branch created
- [x] Legacy `main` preserved
- [x] Claude remediation report reviewed
- [x] Candidate ZIP inventory recorded
- [x] Candidate file hashes recorded
- [ ] Remediated files transferred to working branch
- [ ] File-level verification completed
- [ ] Block 0 closed
