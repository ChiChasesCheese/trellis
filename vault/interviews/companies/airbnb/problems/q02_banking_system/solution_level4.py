"""Level 4 standard answer: solution_level3.py + a balance history per account id and a merge."""
from bisect import bisect_right

from banking_system import BankingSystem

DAY_MS = 24 * 60 * 60 * 1000


class BankingSystemImpl(BankingSystem):
    def __init__(self):
        self.balances = {}  # account_id -> balance
        self.activity = {}  # account_id -> total value of successful transactions
        self.pending = {}   # transfer_id -> [source, target, amount, expires_at], in creation order
        self.transfer_count = 0
        self.history = {}   # account_id -> [(timestamp, balance or None)]; None = the id stopped existing

    def _set_balance(self, account_id, timestamp, balance):
        # The only place a balance changes, so the history cannot miss a write.
        self.balances[account_id] = balance
        self.history[account_id].append((timestamp, balance))

    def _expire(self, timestamp):
        # Every public method calls this first: refunds land before anything reads a balance.
        for transfer_id, (source, _, amount, expires_at) in list(self.pending.items()):
            if timestamp <= expires_at:   # real tests: still pending at exactly t + 1 day
                continue
            # Recorded at the moment it expired (first ms after expires_at), not at the query that noticed it.
            self._set_balance(source, expires_at + 1, self.balances[source] + amount)
            del self.pending[transfer_id]

    def create_account(self, timestamp: int, account_id: str) -> bool:
        self._expire(timestamp)
        if account_id in self.balances:
            return False
        self.history.setdefault(account_id, [])
        self._set_balance(account_id, timestamp, 0)
        self.activity[account_id] = 0
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._expire(timestamp)
        if account_id not in self.balances:
            return None
        self._set_balance(account_id, timestamp, self.balances[account_id] + amount)
        self.activity[account_id] += amount
        return self.balances[account_id]

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._expire(timestamp)
        if account_id not in self.balances or self.balances[account_id] < amount:
            return None
        self._set_balance(account_id, timestamp, self.balances[account_id] - amount)
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
        self._set_balance(source_account_id, timestamp, self.balances[source_account_id] - amount)
        self.transfer_count += 1
        transfer_id = f"transfer{self.transfer_count}"
        self.pending[transfer_id] = [source_account_id, target_account_id, amount, timestamp + DAY_MS]
        return transfer_id

    def accept_transfer(self, timestamp: int, account_id: str, transfer_id: str) -> bool:
        self._expire(timestamp)
        if transfer_id not in self.pending or self.pending[transfer_id][1] != account_id:
            return False
        source, target, amount, _ = self.pending.pop(transfer_id)
        self._set_balance(target, timestamp, self.balances[target] + amount)
        self.activity[source] += amount
        self.activity[target] += amount
        return True

    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        self._expire(timestamp)
        if (account_id_1 == account_id_2
                or account_id_1 not in self.balances
                or account_id_2 not in self.balances):
            return False
        for transfer_id, entry in list(self.pending.items()):
            source, target, amount, _ = entry
            if source == account_id_2 or (source == account_id_1 and target == account_id_2):
                self._set_balance(source, timestamp, self.balances[source] + amount)
                del self.pending[transfer_id]
            elif target == account_id_2:
                entry[1] = None   # spec: stays pending, can never be accepted, refunds when it expires
        self._set_balance(account_id_1, timestamp,
                          self.balances[account_id_1] + self.balances.pop(account_id_2))
        self.activity[account_id_1] += self.activity.pop(account_id_2)
        self.history[account_id_2].append((timestamp, None))
        return True

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        self._expire(timestamp)
        events = self.history.get(account_id, [])
        i = bisect_right(events, time_at, key=lambda event: event[0])
        return events[i - 1][1] if i else None
