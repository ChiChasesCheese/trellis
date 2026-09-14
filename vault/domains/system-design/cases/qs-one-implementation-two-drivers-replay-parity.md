---
nodes:
- async.streaming
title: 'One implementation, two drivers: replay/live parity'
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0008-live-event-driven-nautilus-not-lean
---

# One implementation, two drivers: replay/live parity

The recurring trap in systems that both replay history and run live is two implementations of one logic that drift — the offline one is what you measured, the online one is what acts.

Parity is achievable only when every output depends solely on the prefix of the stream. Given that, feeding the code a truncated prefix at each step must reproduce exactly what the whole-history pass produced at that index. That identity is testable offline and cheaply, before any socket is involved, which converts "probably the same" into a property. It also reframes the ban on lookahead: it is not only statistical hygiene, it is the precondition for streaming the same code at all.

With the property in hand, adopting an engine whose simulation and production modes share one architecture buys parity, venue adapters and reconciliation reports instead of hand-building an order bus and its recovery paths.

But keep two tiers deliberately: a cheap approximate engine for the search loop and a faithful one for execution. A measured 74x per-run gap — widening with data volume — does not mean "slower", it means nobody will run the full sweep, and the honest trial count quietly starts lying.

Finally, order the work: reconciliation at startup that halts on mismatch, persisted order lifecycle with idempotent recovery, and a runtime kill switch come before any new capability.
