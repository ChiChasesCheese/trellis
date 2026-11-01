# Card agent — TikTok 高频设计题 (sub-deck `tt` of the Hello Interview deck)

Follow `research/hello-interview/QB_AGENT.md` exactly (shared body format, own words, gates), with these differences:

- **Your questions** are slugs in your group file; their English prompt is `title_en` in
  `research/hello-interview/tiktok_selection.json`. There is no Hello Interview source file. Sources, read before
  writing: `research/companies/tiktok/catalog/system_design.md` (what TikTok interviewers pushed on, per prompt),
  `vault/interviews/companies/tiktok/05-payment-domain.md` (money flow, ledger, idempotency, reconciliation, refunds,
  FX, PayLater — Chi's own study notes; link it), `vault/interviews/companies/tiktok/07-class-design.md` (the five
  payment class-design exercises; the low-level ones here are those, written as complete answers), and
  `research/companies/tiktok/catalog/payment_loop.md`. Design to the senior bar; put the TikTok follow-ups from
  system_design.md into **取舍与追问**.
- **Payments correctness first** where it applies: integer minor units, append-only ledger, state machines,
  idempotency keys, exactly-once effects, reconciliation, async settlement and webhooks, refunds and chargebacks.
- **Links:** besides concept wikilinks from `concept_index.md`, link the TikTok coding variants that train the same
  mechanism (`vault/interviews/core/leetcode/problems/tt-*.md`, e.g. `[[tt-idempotent-versioned-update|幂等的版本化更新]]`,
  `[[tt-rate-limiter-implementation|手写限流器]]`, `[[tt-lru-cache-ttl|带 TTL 的 LRU]]`, `[[tt-kv-store-snapshot-restore|KV 快照]]`,
  `[[tt-currency-conversion-queries|汇率换算]]`) and the related question-bank answers
  (`vault/interviews/core/design-questions/<slug>.md`) in **同类题**.
- **Meta file:** `research/hello-interview/tt_meta_<group>.json` (same shape as qb_meta).
