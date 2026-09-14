---
nodes:
- correctness.idempotency
- traffic.rate-limiting
title: Resumable ingestion against a metered API
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0006-eodhd-raw-archive-contract
---

# Resumable ingestion against a metered API

Bulk-pulling a corpus from a metered third-party API poses two problems: staying inside quota, and resuming after an interruption.

Quota is a budget you enforce on the client side. Give each endpoint a cost weight, keep a local counter, and every few hundred calls reconcile against the provider's own reported usage, taking the maximum of the two. A mis-guessed local weight then cannot silently blow through the real cap. When the budget is spent, sleep until the provider's reset boundary rather than retrying into rejections.

Resumption is an append-only completion log: load the recorded keys into a set at startup and skip any unit whose key is present. Two choices make it safe. The key is written only *after* the unit's output is durably on disk, so an interrupted unit leaves no key and is redone whole — key granularity is exactly the amount of work you are willing to repeat. And freshness is encoded in the key: a per-day or per-month stamp makes re-running a no-op until the stamp rolls, while entities that can never change again get a stamp-free key and are frozen forever. There is no `--resume` flag; re-running *is* the resume path.

One trap with incremental appends: re-fetch an overlap window and compare it against what you stored. If the source restated the series, refetch it whole rather than concatenating two incompatible bases into one file.
