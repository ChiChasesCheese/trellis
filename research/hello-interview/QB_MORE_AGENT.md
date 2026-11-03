# Question agent — new design questions from the full bank

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents, write only your questions' files. Scratch in `/tmp/qm_<group>/`.
`git checkout uv.lock` whenever uv touches it. **Resume rule:** skip a slug whose body and at least 6 要点 cards already exist.

Chi is a senior candidate. Each question gets one complete answer that fits a 60-minute round and deepens in layers, plus small cards.

## Input

Your slugs are in your group file. The question's text and every report: find it in `sources/local/hello-interview/premium/questions.json` (match `slug`, or the title in
`research/hello-interview/more_selection.json` under `search`); the `upvotes` carry company, level, month and sometimes a candidate's note. Design the answer yourself to the senior bar.

## Output 1 — the body

`vault/domains/hello-interview/premium/bodies/<slug>.md` (gitignored). Same format as a tracked body. Read these models first:
- system design: `vault/interviews/core/design-questions/payment-batch-processing.md`
- low-level design: `vault/interviews/core/design-questions/kv-store-eviction.md`

Follow `research/hello-interview/LEVELS.md` for `**60 分钟路线。**`, 【必讲】/【追问再讲】/【加分】 with at most 3 必讲, and for LLD `**核心实现。**` of about 90 lines with `**逐步扩展。**`.
Frontmatter is only `slug:` and `kind:`. System design prose stays at or under about 3,500 Chinese characters.

**Low-level design:** a drill with tested code may already exist in `vault/interviews/core/low-level-design/problems/<name>/` (see your group file). Reuse its `solution.py`: the core is its first level, the later levels are the extensions. Otherwise
write the code, split it the same way and run it. Quoted outputs must be real.

Every number must be derived or a stated assumption; show the arithmetic once. Wikilinks only to notes that exist in the tracked vault (`research/hello-interview/concept_index.md`).

## Output 2 — small cards

`vault/domains/hello-interview/cards/premium/points/<slug>/`, 8–12 cards, format exactly as in `research/hello-interview/POINTS_AGENT.md`, ids `hi-pt-<slug>-<n>-<short-slug>`, node `points.<slug>`. The header line carries the level:
`**题名 · 要点**｜必会 · 出自：题名 › 部分`. `step:` runs 必会 first, then 追问, then 加分. Facts only from the body.

## Output 3 — meta

Append to `research/hello-interview/more_meta_<group>.json`: `{"<slug>": {"requires": ["sd.core-concepts.caching", "..."]}}` with 2–5 course leaves the answer rests on (ids from `skeleton/hello-interview.yaml`, without `.notes`).

## Style

Chinese with English terms in parentheses on first use. Own words. No site name, no URL, no citation, no process talk. Comments carry the reasoning in code and prose does not repeat it. The style checker rejects 这道题, 本题, 本书, 抓取 and 面经 (even inside 页面经常).

## Gate

`uv run python scripts/plain_style.py <your files>`, `python3 scripts/phone_diagrams.py <your bodies>`, `uv run python research/hello-interview/gen_skeleton.py`, `uv run trellis --domain hello-interview validate` 0 errors.
Reply in ≤ 6 lines: questions done, cards per question, LLD core line counts and what you ran, least sure claims.
