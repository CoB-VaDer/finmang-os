from enum import Enum

class AccountType(str, Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"
    CREDIT = "CREDIT"
    CASH = "CASH"
    E_WALLET = "E_WALLET"

class TransactionType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSFER = "TRANSFER"

class CategoryType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
