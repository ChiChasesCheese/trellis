# q09 Jupyter Load Balancer — report

## Summary
Route long-lived notebook WebSocket connections across `num_targets` Jupyter servers:
least-loaded with smallest-index tie-break, DISCONNECT, sticky object affinity, hard capacity,
and SHUTDOWN with in-order re-routing. It is Stripe's internal notebook platform reduced to a
five-part event-stream simulation; the difficulty is the interaction of the rules (a full sticky
target rejects even when others have room) and making "least loaded" sub-linear at 10^5 targets.

## Sources & confidence
high — 8 independent sources: 1point3acres 题库 `jupyter-load-balancer-oa` (last asked
2026-02-02), 1point3acres thread-1154050 and thread-1147122, prachub
"simulate-sticky-load-balancer-with-shutdown" (full statement + constraints), programhelp
2025-09-30 / 2025-10-16 / 2026-03-16, learncswithus 2025-10-20, cscodehelp stripe-oa-review,
1024bbs 5821.

## Approach by part
State: `load[t]`, a min-heap of `(load, index)` with lazy invalidation, `conns[id] = (user,
obj, target, seq)`, per-target ordered member dicts, `pin[obj] = target`.
1. `least_loaded()` pops stale heap entries until `(load, t)` matches `load[t]`; ties resolve to
   the smallest index because the tuple orders by index second. Duplicate active id → ignore.
2. DISCONNECT: look up the id, decrement, push the new `(load, t)`; unknown id → ignore.
3. If `obj in pin`, the pinned target wins over load; the first placement pins. Pins survive
   disconnects.
4. `load[t] >= cap` is full: the least-loaded target being full means all are; a full sticky
   target rejects regardless of the others. Rejects log nothing.
5. SHUTDOWN: collect members in arrival order (`seq`), clear pins pointing at `t`, mark `t`
   unavailable, re-place each with the same `place()` (logs like CONNECT, drops silently when it
   cannot fit), then `t` rejoins at load 0 (`shutdown_permanent=True` keeps it out).
   `variant_b=True` gives the prachub `CONNECT id obj` / `id target` form.

## Pitfalls hidden tests target
- 1-based target index in the log and in `SHUTDOWN t`; smallest-index tie-break
- sticky target full → reject although other targets have room; `cap` succeed, `cap+1` fails
- duplicate active CONNECT id ignored, id reusable after DISCONNECT; unknown DISCONNECT ignored
- SHUTDOWN re-routes in original arrival order, the first re-routed connection of an object
  re-pins and the rest follow; the shut-down target is not a candidate during its own re-route
  but returns empty afterwards; out-of-range / empty SHUTDOWN is a no-op
- 10^5 targets: scanning all targets per request is O(n·m) — the heap is mandatory

## Complexity & measured cost
O((R + S) log T) with lazy heap entries, O(T + active) memory. 10^5 targets, 2·10^5 mixed
requests (65 % CONNECT, 25 % DISCONNECT, 10 % SHUTDOWN, cap 3): ~0.36 s, ~131 MB RSS
(budget 2 s / 256 MB).
Measured: 0.359s, 131 MB

## Test inventory
24 tests — part1: 5 · part2: 3 · part3: 3 · part4: 3 · part5: 10 (incl. 2 io, 1 perf, the
variant flags); edge 11 · fmt 2 · perf 1 · io 2.
`IMPL=starter`: 23 fail / 1 pass (empty / header-only stdin prints nothing).

## Skills exercised
S01 full-spec reading · S02 parsing · S03 dict-keyed records · S10 ordered event stream with
reversals · S11 idempotent duplicates · S18 ignore paths · S19 incremental design ·
S21 stdlib fluency (heapq, ordered dict)
