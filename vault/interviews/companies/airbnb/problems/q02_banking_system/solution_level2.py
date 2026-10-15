"""Level 2 standard answer: solution_level1.py + an activity counter and one ranking method."""
from banking_system import BankingSystem


class BankingSystemImpl(BankingSystem):
    def __init__(self):
        self.balances = {}  # account_id -> balance
        self.activity = {}  # account_id -> total value of successful transactions

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.balances:
            return False
        self.balances[account_id] = 0
        self.activity[account_id] = 0
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self.balances:
            return None
        self.balances[account_id] += amount
        self.activity[account_id] += amount
        return self.balances[account_id]

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self.balances or self.balances[account_id] < amount:
            return None
        self.balances[account_id] -= amount
        self.activity[account_id] += amount
        return self.balances[account_id]

    def top_activity(self, timestamp: int, n: int) -> list[str]:
        ranked = sorted(self.activity.items(), key=lambda item: (-item[1], item[0]))
        return [f"{account_id}({total})" for account_id, total in ranked[:n]]
