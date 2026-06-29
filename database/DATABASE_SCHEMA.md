# FinMang OS Database Schema

## Purpose

This document defines the logical database structure of FinMang OS.

---

# Core Databases

## 1. Mission

Stores the user's financial mission.

Fields

- Mission Name
- Description
- Start Date
- Target Date
- Status
- Priority

---

## 2. Daily Log

Records daily financial activities.

Fields

- Date
- Mission
- Transportation
- Breakfast
- Lunch
- Dinner
- Drinks
- Other Expense
- Income
- Notes

---

## 3. Budget

Stores monthly budgets.

Fields

- Category
- Planned Amount
- Actual Amount
- Remaining

---

## 4. Assets

Tracks all owned assets.

Fields

- Name
- Category
- Value
- Updated Date

---

## 5. Debts

Tracks liabilities.

Fields

- Name
- Amount
- Due Date
- Status

---

## 6. Automation

Stores automation rules.

Fields

- Name
- Trigger
- Action
- Status

---

Version: 1.0
Status: Official
