# FinMang OS Business Logic

## Purpose

This document defines the business rules, workflows, and operational logic of FinMang OS.

---

# Core Principle

Every financial activity must be:

* Intentional
* Traceable
* Accountable
* Measurable

---

# Financial Flow

Income
↓
Account Balance
↓
Budget Allocation
↓
Expense Recording
↓
Asset / Debt Update
↓
Reports
↓
Archive

---

# Transaction Rules

## Income

* Every income must belong to an account.
* Every income increases account balance.
* Every income is recorded permanently.

---

## Expense

* Every expense belongs to a category.
* Every expense reduces account balance.
* Every expense updates budget usage.
* Expenses cannot exceed available balance without confirmation.

---

## Transfer

* Transfer moves money between accounts.
* Total balance must remain unchanged.
* Both outgoing and incoming records are created.

---

# Budget Rules

* Every month has its own budget.
* Budget starts with Planned Amount.
* Every expense updates Actual Amount.
* Remaining Amount is calculated automatically.
* Overspending triggers a warning.

---

# Asset Rules

* Assets have current value.
* Asset value can increase or decrease.
* Net Worth is calculated automatically.

---

# Debt Rules

* Every debt has a due date.
* Debt payments reduce outstanding balance.
* Paid debts are archived but never deleted.

---

# Automation Rules

Daily

* Prepare Daily Log
* Reset daily counters

Weekly

* Generate weekly report

Monthly

* Close monthly records
* Archive completed month
* Prepare next month's budget

---

# Reporting Rules

Generate:

* Daily Summary
* Weekly Summary
* Monthly Summary
* Budget Report
* Asset Report
* Net Worth Report

---

# General Rules

* No financial record is permanently deleted.
* Every modification is logged.
* Historical records remain searchable.
* All calculations must be reproducible.

---

Version: 1.0

Status: Official
