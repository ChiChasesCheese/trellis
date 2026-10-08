"""Mutation check: each mutant is solution.py with one bug; every one must fail some test."""
import os, pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent)
src = (root / "solution.py").read_text()
M = {
 "create resets balance": ("        if account_id in self.balances:\n            return False\n        self.history.setdefault", "        self.history.setdefault"),
 "pay allows overdraft": ("account_id not in self.balances or self.balances[account_id] < amount:\n            return None\n        self._set_balance(account_id, timestamp, self.balances[account_id] - amount)", "account_id not in self.balances:\n            return None\n        self._set_balance(account_id, timestamp, self.balances[account_id] - amount)"),
 "ties reversed": ("key=lambda item: (-item[1], item[0]))", "key=lambda item: (item[1], item[0]), reverse=True)"),
 "sort as strings": ("key=lambda item: (-item[1], item[0]))", "key=lambda item: str(item[1]), reverse=True)"),
 "activity before pay check": ("    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:\n        self._expire(timestamp)\n", "    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:\n        self._expire(timestamp)\n        if account_id in self.activity: self.activity[account_id] += amount\n"),
 "inclusive expiry": ("if timestamp < expires_at:", "if timestamp <= expires_at:"),
 "expire only on accept": ("    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:\n        self._expire(timestamp)\n", "    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:\n"),
 "activity at transfer time": ("        self.transfer_count += 1\n", "        self.transfer_count += 1\n        self.activity[source_account_id] += amount\n        self.activity[target_account_id] += amount\n"),
 "counter on failed transfer": ("        self._expire(timestamp)\n        if (source_account_id == target_account_id", "        self._expire(timestamp)\n        self.transfer_count += 1\n        if (source_account_id == target_account_id"),
 "accept ignores target": ("if transfer_id not in self.pending or self.pending[transfer_id][1] != account_id:", "if transfer_id not in self.pending:"),
 "merge keeps outgoing": ("if source == account_id_2 or (source == account_id_1 and target == account_id_2):", "if source == account_id_1 and target == account_id_2:"),
 "merge no redirect": ("                entry[1] = account_id_1\n", "                pass\n"),
 "refund dated at query": ("self._set_balance(source, expires_at,", "self._set_balance(source, timestamp,"),
 "get_balance exclusive": ("i = bisect_right(events, time_at,", "i = bisect_right(events, time_at - 1,"),
 "merged id never ends": ("        self.history[account_id_2].append((timestamp, None))\n", ""),
 "between-accounts not cancelled": ("if source == account_id_2 or (source == account_id_1 and target == account_id_2):", "if source == account_id_2:"),
}
killed = 0
for name, (a, b) in M.items():
    assert src.count(a) >= 1, name
    (root / "mutant.py").write_text(src.replace(a, b, 1))
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
                       cwd=root, env={**os.environ, "IMPL": "mutant"}, capture_output=True, text=True)
    last = r.stderr.strip().splitlines()[-1]
    ok = r.returncode != 0
    killed += ok
    print(("KILLED " if ok else "SURVIVED ") + name + " -> " + last)
(root / "mutant.py").unlink()
print(f"{killed}/{len(M)} killed")
