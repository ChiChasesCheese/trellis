"""Level 3 standard answer: solution_level2.py + pending transfers with lazy expiry."""
from banking_system import BankingSystem

DAY_MS = 24 * 60 * 60 * 1000


class BankingSystemImpl(BankingSystem):
    def __init__(self):
        self.balances = {}  # account_id -> balance
        self.activity = {}  # account_id -> total value of successful transactions
        self.pending = {}   # transfer_id -> (source, target, amount, expires_at), in creation order
        self.transfer_count = 0

    def _expire(self, timestamp):
        # Every public method calls this first: refunds land before anything reads a balance.
        for transfer_id, (source, _, amount, expires_at) in list(self.pending.items()):
            if timestamp <= expires_at:   # real tests: still pending at exactly t + 1 day
                continue
            self.balances[source] += amount
            del self.pending[transfer_id]

    def create_account(self, timestamp: int, account_id: str) -> bool:
        self._expire(timestamp)
        if account_id in self.balances:
            return False
        self.balances[account_id] = 0
        self.activity[account_id] = 0
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._expire(timestamp)
        if account_id not in self.balances:
            return None
        self.balances[account_id] += amount
        self.activity[account_id] += amount
        return self.balances[account_id]

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._expire(timestamp)
        if account_id not in self.balances or self.balances[account_id] < amount:
            return None
        self.balances[account_id] -= amount
        self.activity[account_id] += amount
        return self.balances[account_id]

    def top_activity(self, timestamp: int, n: int) -> list[str]:
        self._expire(timestamp)
        ranked = sorted(self.activity.items(), key=lambda item: (-item[1], item[0]))
        return [f"{account_id}({total})" for account_id, total in ranked[:n]]

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str,
                 amount: int) -> str | None:
        self._expire(timestamp)
        if (source_account_id == target_account_id
                or source_account_id not in self.balances
                or target_account_id not in self.balances
                or self.balances[source_account_id] < amount):
            return None
        self.balances[source_account_id] -= amount
        self.transfer_count += 1
        transfer_id = f"transfer{self.transfer_count}"
        self.pending[transfer_id] = (source_account_id, target_account_id, amount, timestamp + DAY_MS)
        return transfer_id

    def accept_transfer(self, timestamp: int, account_id: str, transfer_id: str) -> bool:
        self._expire(timestamp)
        if transfer_id not in self.pending or self.pending[transfer_id][1] != account_id:
            return False
        source, target, amount, _ = self.pending.pop(transfer_id)
        self.balances[target] += amount
        self.activity[source] += amount
        self.activity[target] += amount
        return True
