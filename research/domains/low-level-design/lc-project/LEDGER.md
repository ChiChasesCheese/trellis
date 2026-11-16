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

| Project | Exported | Leaf (commit) | Official tests | Quick cards | Verified | In Anki |
|---|---|---|---|---|---|---|
| rate-limiter | yes | f754fca0 | 6/6 | writing | | synthesis 4 (old layout) |
| return-fraud-risk | yes | 498e211f | 3/3 | writing | | |
| actor-follow-notifications | yes | 498e211f | 3/3 | | | |
| issue-creation-api | yes | 498e211f | 3/3 | | | |
| password-reset | yes | ffacc156 | 4/4 | | | |
| url-shortener | yes | e826c429 | 18 + 24 subtests | | | |
| parcel-return-policy | yes | building | | | | |
| file-deduplication, currency-conversion, sales-reporting | yes | | | | | |
| the other 21 | exporting | | | | | |

Review findings turned into rules (LCP_AGENT.md "Defects found"): per-key parameters for sweeps; no translated
REFLECTION questions; never touch the repo .venv for 3.11; LeetCode wording kept out of public files.
