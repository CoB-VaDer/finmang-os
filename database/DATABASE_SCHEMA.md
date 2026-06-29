# FinMang OS Database Schema

## Purpose

This document defines the logical database structure of FinMang OS.

---

# Core Databases

## 1. Mission

Stores the user's financial missions and goals.

Fields

- id
- Mission Name
- Description
- Category
- Priority
- Status
- Start Date
- Target Date
- Created At
- Updated At

---

## 2. Accounts

Stores all financial accounts.

Fields

- id
- Account Name
- Account Type (Cash, Bank, Wallet, E-Wallet)
- Currency
- Balance
- Status
- Created At
- Updated At

---

## 3. Transactions

Stores every financial transaction.

Fields

- id
- Date
- Account ID
- Mission ID
- Category
- Type (Income / Expense)
- Amount
- Description
- Created At
- Updated At

---

## 4. Budget

Stores monthly budgets.

Fields

- id
- Month
- Category
- Planned Amount
- Actual Amount
- Remaining Amount
- Created At
- Updated At

---

## 5. Assets

Tracks owned assets.

Fields

- id
- Asset Name
- Category
- Current Value
- Purchase Value
- Purchase Date
- Account ID
- Created At
- Updated At

---

## 6. Debts

Tracks liabilities.

Fields

- id
- Debt Name
- Amount
- Due Date
- Status
- Created At
- Updated At

---

## 7. Automation

Stores automation rules.

Fields

- id
- Rule Name
- Trigger
- Action
- Status
- Created At
- Updated At

---

# Relationships

Mission
→ Transactions

Accounts
→ Transactions

Budget
→ Transactions

Accounts
→ Assets

---

Version: 2.0

Status: Official
