"""q10 Payment Intent Commands — reference solution.

One `Ledger` replays commands; every invalid command is ignored silently (the OA never prints
errors).  Parts 1-3 differ only in which command words are enabled.  Part 4 prefixes each line
with a timestamp and uses version-C semantics: CREATE credits the merchant immediately and
REFUND is gated by the merchant's refund window.
"""
from __future__ import annotations

import sys

REQUIRES_ACTION, PROCESSING, COMPLETED = "REQUIRES_ACTION", "PROCESSING", "COMPLETED"

# command word -> number of arguments it accepts. INIT takes exactly 2 in Parts 1-3; only the
# timestamped Part 4 form adds the optional refund_limit (2 or 3). A 3-argument INIT in Parts 1-3
# is a wrong argument count and must be ignored (it must NOT install a refund window).
ARITY = {"INIT": (2,), "CREATE": (3,), "ATTEMPT": (1,), "SUCCEED": (1,),
         "UPDATE": (2,), "FAIL": (1,), "REFUND": (1,)}
ARITY_TIMESTAMPED = {**ARITY, "INIT": (2, 3)}
PART_COMMANDS = {
    1: {"INIT", "CREATE", "ATTEMPT", "SUCCEED"},
    2: {"INIT", "CREATE", "ATTEMPT", "SUCCEED", "UPDATE"},
    3: set(ARITY),
    4: set(ARITY),
}


def _int(s: str) -> int | None:
    """Integer or None (malformed numbers make the whole command a no-op)."""
    try:
        return int(s)
    except ValueError:
        return None


class Payment:
    __slots__ = ("merchant", "amount", "state", "created_at", "refunded")

    def __init__(self, merchant: str, amount: int, state: str, created_at: int):
        self.merchant, self.amount, self.state = merchant, amount, state
        self.created_at, self.refunded = created_at, False


class Ledger:
    def __init__(self, commands: set[str], immediate_credit: bool = False, arity: dict = ARITY):
        self.commands = commands
        self.arity = arity
        self.immediate_credit = immediate_credit
        self.balances: dict[str, int] = {}
        self.limits: dict[str, int | None] = {}   # None = no refund window (always refundable)
        self.payments: dict[str, Payment] = {}

    # ------------------------------------------------------------------ dispatch
    def apply(self, t: int, cmd: str, args: list[str]) -> None:
        if cmd not in self.commands or len(args) not in self.arity.get(cmd, ()):
            return  # unknown word for this part / wrong argument count -> ignore
        getattr(self, "_" + cmd.lower())(t, *args)

    def _transition(self, p: str, src: str, dst: str) -> Payment | None:
        pay = self.payments.get(p)
        if pay is None or pay.state != src:
            return None  # wrong state -> ignore
        pay.state = dst
        return pay

    # ------------------------------------------------------------------ commands
    def _init(self, t, m, balance, limit=None):
        bal, lim = _int(balance), (None if limit is None else _int(limit))
        if m in self.balances or bal is None or (limit is not None and lim is None):
            return  # duplicate INIT never resets the balance
        self.balances[m], self.limits[m] = bal, lim

    def _create(self, t, p, m, amount):
        amt = _int(amount)
        if p in self.payments or m not in self.balances or amt is None or amt < 0:
            return  # duplicate id / unknown merchant / negative amount (0 is fine)
        if self.immediate_credit:  # Part 4 (version C): CREATE completes and credits at once
            self.payments[p] = Payment(m, amt, COMPLETED, t)
            self.balances[m] += amt
        else:
            self.payments[p] = Payment(m, amt, REQUIRES_ACTION, t)

    def _attempt(self, t, p):
        self._transition(p, REQUIRES_ACTION, PROCESSING)

    def _succeed(self, t, p):
        pay = self._transition(p, PROCESSING, COMPLETED)
        if pay is not None:
            self.balances[pay.merchant] += pay.amount  # money moves only on SUCCEED

    def _fail(self, t, p):
        self._transition(p, PROCESSING, REQUIRES_ACTION)

    def _update(self, t, p, amount):
        amt, pay = _int(amount), self.payments.get(p)
        if pay is None or pay.state != REQUIRES_ACTION or amt is None or amt < 0:
            return  # only editable before ATTEMPT; negative ignored
        pay.amount = amt

    def _refund(self, t, p):
        pay = self.payments.get(p)
        if pay is None or pay.state != COMPLETED or pay.refunded:
            return  # only COMPLETED, and only once
        limit = self.limits[pay.merchant]
        # window rule (Part 4): None = always, 0 = never, else t_refund - t_create <= limit (inclusive)
        if limit is not None and (limit == 0 or t - pay.created_at > limit):
            return
        pay.refunded = True
        self.balances[pay.merchant] -= pay.amount

    def render(self) -> list[str]:
        return [f"{m} {self.balances[m]}" for m in sorted(self.balances)]  # plain string order


def _run(lines: list[str], part: int, timestamped: bool, immediate_credit: bool = False) -> list[str]:
    ledger = Ledger(PART_COMMANDS[part], immediate_credit, ARITY_TIMESTAMPED if timestamped else ARITY)
    for raw in lines:
        tokens = raw.split()
        t = 0
        if timestamped:
            if len(tokens) < 2 or _int(tokens[0]) is None:
                continue  # missing / non-integer timestamp -> ignore the line
            t, tokens = _int(tokens[0]), tokens[1:]
        if tokens:
            ledger.apply(t, tokens[0].upper(), tokens[1:])
    return ledger.render()


def part1(lines: list[str]) -> list[str]:
    return _run(lines, 1, timestamped=False)


def part2(lines: list[str]) -> list[str]:
    return _run(lines, 2, timestamped=False)


def part3(lines: list[str]) -> list[str]:
    return _run(lines, 3, timestamped=False)


def part4(lines: list[str], immediate_credit: bool = True) -> list[str]:
    """immediate_credit=False = version-B variant: timestamps + the full Part 1-3 machine."""
    return _run(lines, 4, timestamped=True, immediate_credit=immediate_credit)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 3  # Parts 1-3 accumulate, so the full command set is the default
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
