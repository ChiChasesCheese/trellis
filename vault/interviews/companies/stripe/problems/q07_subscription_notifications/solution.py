"""q07 Subscription Notification Scheduler — reference solution.

Model: every user owns a tiny "pending" list (≤ 3 emails).  An event on day d locks the emails
dated < d (already sent), applies the change, and recomputes the pending list from the new
state, keeping only emails dated >= max(start_day, d).  Output is one global sort with a fully
specified tie-break key.
"""
from __future__ import annotations

import sys

DEFAULT_SCHEDULE = (("start", "Welcome to {plan}"), (-15, "Upcoming expiry"), ("end", "Subscription expired"))
EVENT_KINDS = {"CHANGE", "RENEW"}


class User:
    __slots__ = ("idx", "name", "plan", "start", "end", "since", "sent", "pending")  # 10^5 users: keep it lean

    def __init__(self, idx: int, name: str, plan: str, start: int, end: int):
        self.idx, self.name, self.plan, self.start, self.end = idx, name, plan, start, end
        self.since = start          # emails dated < since are already sent (locked)
        self.sent: tuple = ()        # locked emails: (day, sched_idx, plan_at_send_time); () is a shared singleton
        self.pending: list[tuple] = []

    def recompute(self, schedule) -> None:
        """Pending = schedule emails dated >= start_day and >= last recompute day.
        Only (day, sched_idx, plan) is kept; the text is formatted once at render time."""
        self.pending = []
        for i, (when, _msg) in enumerate(schedule):
            day = self.start if when == "start" else self.end if when == "end" else self.end + int(when)
            if day >= self.start and day >= self.since:  # rule: never before start, never in the past
                self.pending.append((day, i, self.plan))

    def apply_event(self, day: int) -> None:
        """Events take effect at the START of `day`: emails dated < day are locked as sent;
        the caller mutates state and recompute()s, which replaces the pending (>= day) ones."""
        self.sent += tuple(e for e in self.pending if e[0] < day)
        self.since = max(self.since, day)


def _split(raw: str) -> list[str]:
    return [p.strip() for p in raw.split(",")]


def _run(lines: list[str], schedule, allow_change: bool, allow_renew: bool) -> list[str]:
    users: dict[str, User] = {}
    events: list[tuple[int, int, str]] = []  # (day, input_idx, raw line) -- re-split later, keeps memory flat
    for raw in lines:
        f = _split(raw)
        if not raw.strip():
            continue
        if f[0] in EVENT_KINDS:
            if (f[0] == "CHANGE" and allow_change) or (f[0] == "RENEW" and allow_renew):
                events.append((int(f[3]), len(events), raw))
            continue
        name, plan, start, dur = f[0], f[1], int(f[2]), int(f[3])
        users.pop(name, None)  # repeated name: later record wins and takes the later position
        users[name] = User(len(users), name, plan, start, start + dur)  # end = start + duration
    for i, u in enumerate(users.values()):
        u.idx = i
        u.recompute(schedule)

    out: list[tuple] = []  # sort key: (day, user_idx, 0=event/1=email, seq) ; then payload
    for day, seq, raw in sorted(events):  # day order, ties by input index
        f = _split(raw)
        u = users.get(f[1])
        if u is None:
            continue  # unknown user: ignored
        u.apply_event(day)
        if f[0] == "CHANGE":
            old, u.plan = u.plan, f[2]
            u.recompute(schedule)  # welcome (if still pending) must name the new plan
            out.append((day, u.idx, 0, seq, f"{day}: [Changed] {u.name} - {old} -> {u.plan}"))
        else:
            old, u.end = u.end, u.end + int(f[2])  # term extends from the OLD end
            u.recompute(schedule)
            out.append((day, u.idx, 0, seq, f"{day}: [Renewed] {u.name} - {old} -> {u.end}"))
    del events  # free the event rows before the big sort
    for u in users.values():
        for day, i, plan in (*u.sent, *u.pending):
            out.append((day, u.idx, 1, i, plan))  # email payload = plan at send time (shared str)
    out.sort()  # tuples compare on (day, user_idx, kind, seq) first; no key= -> no 4·10^5 temp key tuples
    names = {u.idx: u.name for u in users.values()}
    return [t[4] if t[2] == 0 else f"{t[0]}: {names[t[1]]} - {schedule[t[3]][1].format(plan=t[4])}"
            for t in out]


def part1(lines: list[str], schedule=DEFAULT_SCHEDULE) -> list[str]:
    return _run(lines, schedule, allow_change=False, allow_renew=False)


def part2(lines: list[str], schedule=DEFAULT_SCHEDULE) -> list[str]:
    return _run(lines, schedule, allow_change=True, allow_renew=False)


def part3(lines: list[str], schedule=DEFAULT_SCHEDULE) -> list[str]:
    return _run(lines, schedule, allow_change=True, allow_renew=True)


def schedule_by_rules(current_day: int, accounts: list[tuple[str, int, int]],
                      rules: list[tuple[str, str, int, str]]) -> list[str]:
    """Part 4 (prachub variant). Index accounts by created/expires day so cost is O(A + R + out)."""
    by_created: dict[int, list[int]] = {}
    by_expires: dict[int, list[int]] = {}
    for i, (_, created, expires) in enumerate(accounts):
        by_created.setdefault(created, []).append(i)
        by_expires.setdefault(expires, []).append(i)
    hits: list[tuple[int, int]] = []  # (account_idx, rule_idx)
    for r, (_, trigger, offset, _) in enumerate(rules):
        if trigger == "on_create":               # current == created + offset
            matched = by_created.get(current_day - offset, [])
        elif trigger == "days_before_expiration":  # current == expires - offset
            matched = by_expires.get(current_day + offset, [])
        elif trigger == "after_expiration":      # current == expires + offset
            matched = by_expires.get(current_day - offset, [])
        else:
            raise ValueError(f"unknown trigger {trigger!r}")
        hits += [(a, r) for a in matched]
    hits.sort()  # account input order, then rule configuration order
    return [f"{accounts[a][0]} {rules[r][0]} {rules[r][3]}" for a, r in hits]


def part4(lines: list[str]) -> list[str]:
    current_day = int(lines[0].strip())
    accounts, rules = [], []
    for raw in lines[1:]:
        f = [p.strip() for p in raw.split(",", 4)]  # template keeps its own commas
        if f[0] == "ACCOUNT":
            accounts.append((f[1], int(f[2]), int(f[3])))
        elif f[0] == "RULE":
            rules.append((f[1], f[2], int(f[3]), f[4]))
    return schedule_by_rules(current_day, accounts, rules)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = 3  # no PART header -> full rule set (Part 3 is a superset of 1 and 2)
    if lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines)
    stdout.writelines(line + "\n" for line in out)  # stream: no second 25 MB joined copy of the output


if __name__ == "__main__":
    main()
