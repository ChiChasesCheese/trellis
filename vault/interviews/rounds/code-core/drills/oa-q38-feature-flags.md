---
nodes: [verification.determinism, model.state-machine, transfer.stripe-oa]
tags: [stripe-oa, q38]
---
# Drill: evaluate a feature flag for a user through kill switch, lists, attributes, rollout and dependencies

Sixty minutes, stdin to stdout, one accumulating program. `FLAG` lines
declare a feature with a set of optional rules (allow/deny lists, a
percentage rollout, attribute rules, other flags it requires); `USER` lines
declare a user's attributes; `CHECK` lines ask whether a flag is ON for a
user, and re-declaring a `FLAG` or `USER` replaces it. The rules interact in
a fixed evaluation order, and the point of the exercise is getting that order
right, not the data structures. Part 1 is the kill switch plus allow/deny
lists. Part 2 adds a deterministic percentage rollout keyed by a stable hash
of flag and user. Part 3 adds attribute targeting (country, plan, and an A/B
rule on even user ids) ANDed across keys and ORed within a key. Part 4 adds
`requires`, a dependency on other flags evaluated recursively, checked before
the allow/deny lists so even an allowlisted user needs its prerequisites.

**Constraints to state and honor**
- Commands: `FLAG,<name>,<on|off>[,<option>]...`, `USER,<id>[,<key>=<value>]...`,
  `CHECK,<flag>,<user>` — options in any order, each at most once.
- An unknown flag is OFF; a `CHECK` for an unknown user treats it as having
  no attributes.
- The evaluation order is fixed: unknown flag / kill switch / dependency
  chain beat the allow list; deny beats allow; allow bypasses attributes and
  rollout but not dependencies.
- The rollout bucket must come from a stable hash (crc32 or similar) over
  both flag name and user id, never the built-in `hash()`, since it must be
  reproducible across runs.
- `requires` is recursive, and a missing flag or a dependency cycle must
  resolve to OFF, not error.

**Grading points**
- Say the evaluation order out loud before coding it — it's the whole
  problem, and it's easy to reorder allow/deny/rollout by instinct instead of
  by the spec.
- An allowlist is a bypass, not the sole audience: a user off every list
  still falls through to attribute rules and rollout, and the worked
  examples catch a design that treats allow as exclusive.
- The rollout boundary is a strict `<`, not `≤`, against the bucket, and
  `rollout=0`/`100` are real values to test, not just the middle.
- `requires` needs a `seen` set to catch cycles, and must be checked before
  deny/allow per the stated order.
- Re-declaring a `FLAG` or `USER` fully replaces the old definition — don't
  merge new options into old ones.
- OR within a key, AND across keys, and a user missing the key entirely
  fails the rule — three different failure shapes worth naming separately.

**Source**
- `vault/stripe/q38_feature_flags/question.md`, `vault/stripe/q38_feature_flags/solution.md`, `vault/Quick_Check/problems/q38_feature_flags/problem.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
