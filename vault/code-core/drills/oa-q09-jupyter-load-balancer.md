---
nodes: [toolbox.heap, performance.budget, transfer.stripe-oa]
tags: [stripe-oa, q09]
---
# Drill: route sticky, capacity-limited connections across a fleet with shutdowns

Sixty minutes, stdin to stdout, no libraries beyond the standard one. A load
balancer sits in front of `num_targets` identical servers, each with a
connection capacity. Requests arrive as `CONNECT id user [object]`,
`DISCONNECT id`, and `SHUTDOWN target` (1-based). Simulate the balancer and
print one line per successful placement, in the order placements happen. The
rules accumulate into a single program (no `PART n` line).

- Part 1: route each CONNECT to the least-loaded target, ties broken by
  smallest index; a CONNECT reusing an already-active id is a silent no-op.
- Part 2: add DISCONNECT — decrement the owning target's load; unknown or
  already-disconnected ids are silently ignored, and ids may be reused later.
- Part 3: add object affinity — a CONNECT carrying an object id that has
  already been placed must go to that same target regardless of load; the
  pin survives disconnects and is cleared only by that target's shutdown.
- Part 4: add hard capacity — a full target can't be chosen; if the sticky
  target for an object is full, that CONNECT is rejected even when other
  targets have room.
- Part 5: add SHUTDOWN — evict every connection on a target, clear any object
  pins pointing at it, then re-route the evicted connections one at a time in
  their *original* CONNECT arrival order under the same rules, after which
  the target rejoins the pool empty.

**Constraints to state and honor**
- Up to ~10^5 targets and ~2*10^5 requests; capacities up to 10^9 — "pick the
  least-loaded target" must not scan every target per request.
- Target indices are 1-based everywhere, in output and in `SHUTDOWN`.
- Only successful CONNECTs and successful shutdown re-routes are logged;
  DISCONNECT, SHUTDOWN, duplicates, and rejections produce no output.
- During its own shutdown, the target being drained is not itself a
  candidate for the re-routing that follows.

**Grading points**
- Least-loaded selection implemented with a min-heap of `(load, index)` and
  lazy deletion (an entry is stale, and skipped, whenever it doesn't match
  the target's current load) — not a linear scan, which is explicitly called
  out as too slow at the stated scale.
- A full sticky target rejects its CONNECT even when other targets have
  room — a candidate should articulate why affinity overrides load-balancing
  but not capacity.
- Capacity boundary exercised exactly: the `cap`-th connection to a target
  succeeds, the `(cap+1)`-th fails.
- SHUTDOWN re-routes connections in the order they originally arrived
  (tracked separately from which target they currently sit on), clears
  object pins for that target *before* re-routing so the first re-routed
  connection of an object re-establishes the pin and later ones for the same
  object follow it, and the drained target returns to the pool at load zero.
- A re-routed connection that finds no room anywhere is simply dropped
  (no longer active, no output) rather than erroring or blocking the rest.
- Idempotency and ignore-paths are explicit: duplicate active CONNECT ids,
  unknown DISCONNECT ids, and out-of-range or empty-target SHUTDOWNs are all
  named as no-ops a candidate should test for.

**Source**
- `vault/stripe/q09_jupyter_load_balancer/question.md`
- `vault/stripe/q09_jupyter_load_balancer/solution.md`
- `vault/Quick_Check/problems/q09_jupyter_load_balancer/problem.md`
- `vault/Quick_Check/problems/q09_jupyter_load_balancer/REPORT.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
