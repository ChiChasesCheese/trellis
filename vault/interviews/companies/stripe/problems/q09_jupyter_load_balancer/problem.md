# q09 · Jupyter Load Balancer — route WebSocket connections across notebook servers

**Type:** bespoke OA · **Stage:** HackerRank OA (60 min, 5 progressive parts) · **Last asked:** 2026-02-02 (1point3acres 题库)
**Frequency:** 8 independent sources (1point3acres thread-1154050, thread-1147122, 题库 `jupyter-load-balancer-oa`; learncswithus 2025-10-20; programhelp 2025-09-30 / 2025-10-16 / 2026-03-16; cscodehelp; prachub full statement; 1024bbs 5821 mention) · **Confidence:** high

## Context
Stripe's internal Notebook platform runs on Jupyter. One server per team degraded under load, so
the platform now runs `num_targets` identical Jupyter servers behind a load balancer. Every
notebook open in a browser is a long-lived WebSocket **connection**; the balancer decides which
server (target) accepts it. Notebook kernels are stateful, so all connections that touch the same
notebook **object** must land on the same server. Servers have a hard connection **capacity** and
are occasionally **shut down** for maintenance, at which point their connections must be moved.

## Input (stdin)
Line 1: `num_targets max_connections_per_target` (integers). Then one request per line, in order.
Blank lines are ignored. Extra spaces between tokens are tolerated.

```
CONNECT <connectionId> <userId> [<objectId>]
DISCONNECT <connectionId>
SHUTDOWN <targetIndex>            # 1-based
```
Constraints (prachub): 1 ≤ num_targets ≤ 10^5, ≤ 2·10^5 requests, 1 ≤ capacity ≤ 10^9.

Function form: `route_requests(num_targets, max_connections_per_target, requests) -> list[str]`.

## Output
One line `connectionId,userId,targetIndex` (**target 1-based**, no spaces) for every **successful**
CONNECT and for every successful re-route after a SHUTDOWN, in the order the placements happen.
Rejected/dropped connections, DISCONNECT and SHUTDOWN produce no output. The rules accumulate —
the final program handles every part; there is no `PART n` line.

## Rules
### Part 1 — least-loaded routing
Each CONNECT goes to the target with the fewest **active** connections; ties → smallest index.
A CONNECT whose `connectionId` is already active is a duplicate and is ignored (no log, no change).

### Part 2 — DISCONNECT
`DISCONNECT id` finds the target holding `id` and decrements its active count. An unknown or
already-disconnected id is ignored (no error, no output). The id may be reused by a later CONNECT.

### Part 3 — object affinity (sticky)
If a CONNECT carries an `objectId` that has already been routed, it must go to the **same target**
even if that target is more loaded. The first connection for an object is placed by the Part 1
rule and pins the object to that target. The pin **survives disconnects** (a kernel stays where
it was started); it is only cleared by a SHUTDOWN of that target.

### Part 4 — capacity
A target with `max_connections_per_target` active connections cannot be chosen. If no target has
room the CONNECT is rejected (no log). If the sticky target of an object is full the CONNECT is
rejected **even if other targets have room** (no log).

### Part 5 — SHUTDOWN
`SHUTDOWN t` evicts every active connection on target `t` and re-routes them one by one **in their
original CONNECT arrival order** using exactly the rules above (least-loaded with tie-break,
object affinity, capacity). Object pins that pointed at `t` are cleared first, so the first
re-routed connection of an object picks a fresh target and the rest of that object follow it.
While re-routing, target `t` is unavailable; afterwards it **rejoins the pool with load 0**
(prachub). A re-routed connection that cannot be placed is dropped (it is no longer active; no
log). Each successful re-route is logged like a CONNECT. SHUTDOWN of an out-of-range index is
ignored.

## Worked examples
### Example 1 (Parts 1–2) — `3 10`
```
CONNECT c1 u1        -> c1,u1,1
CONNECT c2 u2        -> c2,u2,2
CONNECT c3 u3        -> c3,u3,3
CONNECT c4 u4        -> c4,u4,1      (all at 1 → smallest index)
DISCONNECT c2                        (target 2 back to 0)
CONNECT c5 u5        -> c5,u5,2
DISCONNECT nope                      (unknown → ignored)
CONNECT c6 u6        -> c6,u6,2      (loads 2,1,1 → smallest index among the 1s)
```
### Example 2 (Parts 3–4) — `2 2`
```
CONNECT c1 u1 nb1    -> c1,u1,1      (nb1 pinned to 1)
CONNECT c2 u2        -> c2,u2,2
CONNECT c3 u3 nb1    -> c3,u3,1      (sticky; target 1 now full)
CONNECT c4 u4 nb1                    (sticky target full → rejected)
CONNECT c5 u5        -> c5,u5,2      (target 1 full → 2; now full)
CONNECT c6 u6                        (all full → rejected)
DISCONNECT c2                        (target 2 → 1)
CONNECT c7 u7 nb1                    (sticky target 1 still full → rejected although 2 has room)
CONNECT c8 u8        -> c8,u8,2
```
### Example 3 (Part 5) — `3 2`
```
CONNECT c1 u1 nbA    -> c1,u1,1
CONNECT c2 u2        -> c2,u2,2
CONNECT c3 u3 nbA    -> c3,u3,1      (target 1 full)
CONNECT c4 u4        -> c4,u4,3
SHUTDOWN 1           -> c1,u1,2      (evict c1,c3; nbA unpinned; loads 2:1 3:1 → c1 to 2, pins nbA;
                                      target 2 now full → c3 sticky to 2 → dropped; target 1 rejoins at 0)
CONNECT c5 u5        -> c5,u5,1      (loads 0,2,1)
CONNECT c6 u6 nbA                    (sticky 2 full → rejected)
DISCONNECT c1                        (target 2 → 1)
CONNECT c7 u7 nbA    -> c7,u7,2
```
With the *permanent* shutdown variant (target 1 removed) the same input yields
`... c1,u1,2 / c5,u5,3 / c7,u7,2` (c5 goes to 3 because 1 is gone and 2 is full).

## Edge cases hidden tests are known to target
- 1-based target index in the log and in `SHUTDOWN t`; the tie-break is *smallest index*
- DISCONNECT of an unknown / already-disconnected id → silently ignored
- duplicate CONNECT id while active → ignored; same id may be reused after DISCONNECT
- sticky target full → reject even though other targets have room (no log line)
- capacity exactly reached (`load == cap`) is full; `cap` connections succeed, the `cap+1`-th fails
- SHUTDOWN re-routing order is original arrival order, and re-routed connections keep sticking
  to each other (object pin re-established by the first one placed)
- the shut-down target is not a candidate during its own re-routing but rejoins at load 0 after
- SHUTDOWN of an empty or out-of-range target is a no-op
- 10^5 targets × 2·10^5 requests: "least loaded" must not scan all targets per request (heap
  with lazy invalidation)

## Variants seen in the wild
- **prachub (variant B)**: `CONNECT connectionId objectId` (every connection is sticky, no user)
  and the log is `connectionId serverIndex` (space-separated). Supported by `variant_b=True`.
- **programhelp**: a shut-down target is removed from the pool permanently; connections that do not
  fit are dropped. Supported by `shutdown_permanent=True`.
- 1point3acres 题库 summary words the parts as "round-robin → duplicate-aware → disconnects →
  capacity limits → SHUTDOWN"; least-loaded-with-smallest-index is round-robin while nobody
  disconnects, and duplicate CONNECT ids are handled by the Part 1 rule above.

## What this tests
skills: S01 read the whole spec · S02 parsing · S03 modelling with dict-keyed records ·
S10 ordered event stream with reversals · S11 idempotent duplicates · S18 validation/ignore paths ·
S19 incremental design · S21 stdlib fluency (heapq, dict order)

## Sources
- 1point3acres 题库 `company/stripe/jupyter-load-balancer-oa` (OA · 60 min · Medium · last asked 2026-02-02)
- 1point3acres thread-1154050 「【求米】Stripe 2025 SWE Intern OA分享（含笔记）」
- 1point3acres interview/thread/1147122 「Server Load Balancer Design」
- prachub.com/coding-questions/simulate-sticky-load-balancer-with-shutdown (full statement, constraints)
- programhelp.net 2025-09-30, 2025-10-16, 2026-03-16/17 (NG OA write-ups)
- learncswithus.com 2025-10-20 「Stripe SDE NG OA 原题」
- cscodehelp.com/stripe/stripe-oa-review
- 1024bbs 5821 (mention)

## Clarifications (from adversarial review, 2026-08-26)
- A second `SHUTDOWN` re-routes evicted connections in their ORIGINAL `CONNECT` arrival order (global sequence), not in the order they landed on the shut-down target.
