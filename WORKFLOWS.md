# FinMang OS - Workflows

Version: 1.0
Status: Draft

---

## MVP Workflows (Phase 1)

### 1. Add Income
1. User opens CLI or UI.
2. User selects "Add Income".
3. User enters amount.
4. User selects category (e.g., Salary).
5. User adds optional description.
6. System creates Transaction (type: INCOME).
7. System updates Account balance.
8. System confirms: "Income added."

---

### 2. Add Expense
1. User opens CLI or UI.
2. User selects "Add Expense".
3. User enters amount.
4. User selects category (e.g., Groceries).
5. User adds optional description.
6. System creates Transaction (type: EXPENSE).
7. System updates Account balance.
8. System confirms: "Expense added."

---

### 3. View Balance
1. User requests balance.
2. System sums all INCOME transactions.
3. System sums all EXPENSE transactions.
4. System calculates (Income - Expense).
5. System displays total balance.

---

### 4. List Transactions
1. User requests transaction list.
2. System retrieves all Transactions.
3. System displays them (date, category, amount, description).

---

## Future Workflows (Phase 2+)
- Recurring transactions (Automation Engine)
- Budget creation and tracking
- Asset management
- Debt management
- Report generation

---

## Workflow Rules
- Every transaction must link to an Account and a Category.
- Balance is always real-time (calculated from transactions).
- No deletion in MVP (soft delete only).
