"""q07 Subscription Notification Scheduler — YOUR implementation. Run: python drill.py test q07"""
from __future__ import annotations

import sys

# (when, message) pairs; when ∈ {"start", "end"} or a negative int = days before the end day.
DEFAULT_SCHEDULE = (("start", "Welcome to {plan}"), (-15, "Upcoming expiry"), ("end", "Subscription expired"))


def part1(lines: list[str], schedule=DEFAULT_SCHEDULE) -> list[str]:
    """lines: 'name,plan,start_day,duration_days'. Return ['day: name - message', ...]."""
    # TODO
    return []


def part2(lines: list[str], schedule=DEFAULT_SCHEDULE) -> list[str]:
    """Part 1 + 'CHANGE,name,new_plan,day' events -> 'day: [Changed] name - old -> new'."""
    # TODO
    return []


def part3(lines: list[str], schedule=DEFAULT_SCHEDULE) -> list[str]:
    """Part 2 + 'RENEW,name,extra_days,day' events -> 'day: [Renewed] name - old_end -> new_end'."""
    # TODO
    return []


def schedule_by_rules(current_day: int, accounts: list[tuple[str, int, int]],
                      rules: list[tuple[str, str, int, str]]) -> list[str]:
    """Part 4. accounts: (account_id, created_day, expires_day); rules: (name, trigger, offset_days,
    template). Return ['account_id rule_name template', ...] (account order, then rule order)."""
    # TODO
    return []


def part4(lines: list[str]) -> list[str]:
    """lines[0] = current_day; then 'ACCOUNT,id,created,expires' / 'RULE,name,trigger,offset,template'."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = 3  # no PART header -> full rule set
    if lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
