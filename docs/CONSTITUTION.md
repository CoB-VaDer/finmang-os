# FinMang OS Constitution

Version: 1.0
Status: Draft

---

# Purpose

This Constitution is the governing document of FinMang OS.

It defines the engineering principles, development workflow, quality standards, documentation rules, and decision-making process that govern the project.

All project documents, architectural decisions, and implementations must align with this Constitution.

If any document conflicts with this Constitution, the Constitution takes precedence.
---

# Project Governance

The following rules govern all development activities within FinMang OS.

1. Follow the official roadmap. Phases and dependencies must not be skipped.

2. Design before implementation. Business rules and architecture must be defined before code is written.

3. Every major architectural decision must be documented.

4. Documentation is part of the product and must be maintained alongside the code.

5. Production quality takes precedence over shortcuts.

6. AI provides recommendations and engineering guidance. Final decisions belong to the project owner.

7. Every completed task must have a clear Definition of Done before the next task begins.git add .
---

# Engineering Philosophy

FinMang OS is developed according to the following engineering principles:

- Business before technology.
- Architecture before implementation.
- Simplicity over unnecessary complexity.
- Modular design over tightly coupled systems.
- Automation over repetitive manual work.
- Documentation evolves with the project.
- Maintainability is prioritized over short-term speed.
- Every feature must contribute to a production-quality system.
---

# Documentation Standards

Every project document has a single responsibility.

- CONSTITUTION.md governs the project.
- PROJECT_CHARTER.md defines project purpose and scope.
- VISION.md defines the long-term direction.
- MISSION.md defines the ongoing purpose.
- BUSINESS_LOGIC.md defines business rules.
- ARCHITECTURE.md defines the technical design.
- ROADMAP.md defines project execution.
- STATE.md records the current project status.

Information should exist in one authoritative document only. Duplicate documentation should be avoided.
---

# Development Workflow

Every feature follows this workflow:

1. Define the business requirement.
2. Update or create the business rules.
3. Design the architecture.
4. Implement the code.
5. Test the implementation.
6. Review the changes.
7. Update the documentation.
8. Commit and push the changes.
---

# Quality Gates

Before any work is considered complete:

- Business rules are validated.
- Architecture remains consistent.
- Documentation is updated.
- Code follows project standards.
- Changes are tested.
- Git history is clean with meaningful commit messages.
- The Definition of Done is satisfied.
---

# Decision Management

Major architectural and engineering decisions must be recorded before implementation.

Rules:

- Every significant decision requires an Architecture Decision Record (ADR).
- Each ADR must include the context, decision, rationale, and consequences.
- ADR files are stored in `docs/ADR/`.
- Existing ADRs must not be rewritten. If a decision changes, create a new ADR that supersedes the previous one.
---

# Roadmap Governance

The project roadmap is the official execution plan.

Rules:

- Development follows approved phases.
- Dependencies must not be skipped.
- Each sprint has defined objectives and deliverables.
- A phase is complete only after its Definition of Done is met.
- Changes to the roadmap must be reviewed before adoption.
