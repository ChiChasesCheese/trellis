# LeetCode Project → low-level-design: ledger

Pipeline per project (Chi, 2026-11-16): export the workspace (`scripts/lcp_export.py`, local only) → problem leaf
(`proposals/lld/LCP_TASK.md` + `LCP_AGENT.md`: solution passing the official public tests, own tests, article, drill,
3–5 synthesis cards in the dense layout, fine-grained `points.json`) → orchestrator review and commit → quick cards
(`LCP_QUICK_AGENT.md` writer: points + ten-second cards + synthesis-card rewrite) → independent verifier → orchestrator
review → `lcp_quick.py push` → `lcp_plan.py` (view deck `8 LC Project`). Agents: sonnet, at most 3 at a time.

Card design (Chi): vocabulary-style, tap don't type, ≤ 10 s, one fine-grained point per card, extension line outside the
grade, code over prose, dense structured backs with a diagram; every point practised at least twice
(`second_practice.json`). Formats: mc, multi, judge (Kprim), bug (tap the wrong line), order (rank by tap, decoys,
adjacent-swap → Hard), match, cloze, flaw, qa; 不会 button on tapped cards.

Next action: keep three agents busy in this order of priority — a quick writer for a reviewed leaf, a verifier for
written quick cards, a problem agent for the next exported project (study order in the skeleton).

| Project | Leaf (commit) | Official tests | Quick cards (verified, in Anki) |
|---|---|---|---|
| rate-limiter | f754fca0 | 6/6 | 49 |
| return-fraud-risk | 498e211f | 3/3 | 46 |
| actor-follow-notifications | 498e211f | 3/3 | 50 |
| issue-creation-api | 498e211f | 3/3 | 47 |
| password-reset | ffacc156 | 4/4 | 48 |
| url-shortener | e826c429 | 18 + 24 subtests | 51 |
| parcel-return-policy | ea22f091 | 2/2 (workspace Decision) | writing |
| file-deduplication | fedf07dd | 3/3 | writing |
| currency-conversion | b6f6876c | 2/2 | — |
| sales-reporting | 1ecc608b | 2/2 | — |
| reservation-service | building | | |
| exported, not started | keyword-user-blocklists, tool-call-agent, receivable-allocation, scheduled-banking, stack-trace-stream, stockroom-inventory, comments-replies | | |
| export pending | the other 13 (export rerun after the usage limit) | | |

Review findings turned into rules (LCP_AGENT.md "Defects found"): per-key parameters for sweeps; no translated
REFLECTION questions; never touch the repo .venv for 3.11; LeetCode wording kept out of public files.

## 2026-11-16 (evening)

- 题目 / 题目理解 (reading + recall cards, `LCP_READ_AGENT.md`): verified and in Anki for return-fraud-risk,
  actor-follow-notifications, issue-creation-api, password-reset (90 cards, 13 fixed by the verifiers); written for
  file-deduplication, currency-conversion (verifying); writing url-shortener, parcel-return-policy.
- Quick cards verified and in Anki: event-campaigns (48), payment-reconcile-api (51).
- image-transform-pipeline leaf committed (cbaf0c16), 3/3 official tests.
- Workspace copies: `scripts/lcp_overlap.py` found 15 committed leaves repeating workspace text beyond signatures
  (worst: event-campaigns, stockroom-inventory). All unpushed. Rewrite per `proposals/lld/LCP_DECOPY_TASK.md`;
  **no push until every leaf prints ok.**
- `scripts/lcp_preview.py` renders cards with the real templates (screenshot at 390 px with Playwright, channel chrome).

