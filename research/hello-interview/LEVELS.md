# Revise agent — make a design answer fit a 60-minute interview, layered from must-have to bonus

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents, write only your questions' files. Scratch in
`/tmp/lv_<group>/`. `git checkout uv.lock` whenever uv touches it. **Resume rule:** skip a body that already has `**60 分钟路线。**`.

Chi (2026-11-03): the answers read harder than a 60-minute round and lack a sense of what comes first. Each answer must show
what a candidate actually does in 60 minutes and deepen step by step. **The model to copy:**
`vault/interviews/core/design-questions/tt-query-condition-parser.md` and its cards in
`vault/domains/hello-interview/cards/points/tt-query-condition-parser/`. Read them first.

## The body: `vault/interviews/core/design-questions/<slug>.md`

Keep the facts and numbers; this is reorganising and trimming, not new research. Add no claim the body does not already make.

1. Right after **一句话。** add `**60 分钟路线。**`: a small table `| 时间 | 做什么 |`, 4–6 rows, summing to 60 minutes, phone width.
   System design usually: requirements and numbers 5 min, entities and API 5, overall design 15, must-have deep dives 25, follow-ups 10.
   Low-level design usually: clarify and API 8, core code 30–35, run examples 5, follow-ups the rest.
2. **深入。** order by importance, each item starts with 【必讲】, 【追问再讲】 or 【加分】. At most 2–3 【必讲】: what this question
   is really about, and what fits in the time. The rest move down, not out.
3. **取舍与追问。** most likely first; say what is enough to answer orally.
4. **级别期望。** keep; mid-level must be achievable within the route.
5. Trim sentences that repeat another section or the code. System design target: about 4,000 Chinese characters of prose or fewer.
6. **Low-level design code.** `**核心实现。**` is what can be written in 30–35 minutes: about 90 lines at most, the essential classes
   and the one or two key methods, nothing speculative. Anything beyond it goes to `**逐步扩展。**`, numbered, each step tagged 【追问再讲】 or
   【加分】, with the trigger and only the code it adds or changes. Do not rewrite code that already fits. If you cut or split code,
   run it in your scratch folder (the core alone, then with each step) and make sure the outputs quoted on the card are still real.
7. Keep the shared-body format, wikilinks and the other sections as they are. Code comments carry the reasoning.

## The small cards: `vault/domains/hello-interview/cards/points/<slug>/`

Keep each file name and `id` (Chi's review history hangs on it). In the header line, put the level first:
`**题名 · 要点**｜必会 · 出自：题名 › 部分`, with 必会 / 追问 / 加分 matching the tag of what the card covers. Renumber `step:` so 必会 come first,
then 追问, then 加分. Update the 部分 name if the content moved. Change the answer only if it no longer matches the body.

## Gate

`uv run python scripts/plain_style.py <your files>` ok, `python3 scripts/phone_diagrams.py <your bodies>` ok,
`python3 -B scripts/check_wikilinks.py | tail -1` no dead link of yours, `uv run trellis --domain hello-interview validate` 0 errors.
The style checker rejects 这道题, 本题, 本书, 抓取 and 面经 (even inside 页面经常). Reply in ≤ 5 lines: questions done; for low-level design the core line count; anything you could not verify.
