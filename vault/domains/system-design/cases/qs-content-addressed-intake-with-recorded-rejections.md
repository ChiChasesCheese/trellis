---
nodes:
- correctness.idempotency
title: Content-addressed intake, with rejections on the record
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0005-scout-idea-funnel-event-log-agent-triage
---

# Content-addressed intake, with rejections on the record

An intake funnel that pulls candidates from many sources and turns some of them into work has three failure modes: re-fetching creates duplicates, rejected items vanish and are rediscovered forever, and the decisions are unreproducible.

One shape fixes all three. Derive each item's id from a hash of its source plus natural key and store it as one immutable file named by that id: re-harvesting the same item is a no-op, so the fetcher can crash, restart, or run twice with no coordination. This is an idempotency key that the payload carries rather than the caller invents — no dedup window to tune, because identity is intrinsic. Record decisions in a second log, one immutable verdict per item, including rejections and their reasons, so "we looked and said no" is durable, auditable, and prevents a second review. The work queue is then not a mutable status column but a derived set difference: items with no verdict yet.

This replaces the tempting design of one mutable file per day rewritten in place, which loses updates the moment two writers overlap — a race hidden for as long as exactly one writer exists.

The last piece is the seam: deterministic code owns the verbs (harvest, list queue, apply verdict) and stays testable; judgment — score, priority, accept or reject — lives outside it. The cost is two logs and no single row saying "current status".
