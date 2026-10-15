"""Level 1 standard answer: one dict, three methods, nothing else."""
from banking_system import BankingSystem


class BankingSystemImpl(BankingSystem):
    def __init__(self):
        self.balances = {}  # account_id -> balance

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.balances:
            return False
        self.balances[account_id] = 0
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self.balances:
            return None
        self.balances[account_id] += amount
        return self.balances[account_id]

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self.balances or self.balances[account_id] < amount:
            return None
        self.balances[account_id] -= amount
        return self.balances[account_id]
