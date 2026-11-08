# Prerequisite agent: no card may assume a concept Chi was never taught

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents. Scratch in `/tmp/prereq_<group>/`. `git checkout uv.lock`
whenever uv touches it. **Resume rule:** your ledger is the record; skip every card already in it.

Chi met the OAuth PKCE card cold: 「完全不会啊 没接触过这部分内容」. The card was correct, but it assumed OAuth basics, and no deck he
studies taught them. The fix was three foundation cards (OAuth's purpose, the code flow's two channels, public clients)
placed before PKCE: `vault/domains/hello-interview/cards/premium/sdx/more.security/hi-sdx-sec-oauth-{why,code-flow,public-client}.md`.
Read them: they are the model for what you write. Your job is the same check for every merged card in your folders.

## Input

`sources/local/hello-interview/sdx/prereq/<G>.txt` lists your folders under `vault/domains/hello-interview/cards/premium/sdx/`.
Chi studies these decks, so a concept taught in any of them counts as taught:
`vault/domains/{hello-interview,bagu,payments,hft,kafka,low-level-design,snowflake}/cards` and `vault/interviews/core/design-questions`.
The English `system-design` and `cdn-content` decks do not count.

## Per card

1. List the concepts the card takes for granted: the terms its question and answer use without explaining. A backend
   engineer with a few years' experience knows HTTP, SQL, indexes, threads, caches and queues in general; do not list
   those. Do list named mechanisms, protocols and techniques (for example 2PC, quorum, vector clock, SFU, contraction
   hierarchies, Bloom filter, MVCC, ISR, consistent hashing, OIDC).
2. For each one, grep the decks above (English and Chinese terms). It is taught if some card explains what it is and why
   it exists, not just mentions it.
3. One ledger line per card in `sources/local/hello-interview/sdx/prereq/ledger_<G>.jsonl`:
   `{"card": id, "assumes": [...], "taught_in": {concept: path}, "missing": [...], "added": [new ids]}`.

## When something is missing

- Write the foundation card in the same folder, before the card that needs it. Use the shape in
  `research/hello-interview/sdx/SDX_AGENT.md` (title line `**主题**｜补充 · <页面> · 必会`, 结论 / 要点 / 为什么 / 面试里这样说 / 易错).
  Explain from zero, in plain words, with a concrete example. Add a figure when the idea is a flow or a structure.
  Id `hi-sdx-<short-slug>`, unique across `cards/premium/sdx/`.
- One foundation card can serve several cards. If two folders need the same concept, write it once, in the folder
  where it is most at home, and note it in both ledger lines.
- **Order:** renumber `step` in that folder so every foundation card comes before the cards that use it. Steps stay
  1..N with no gaps or repeats. Change only `step:` lines in existing cards; never edit their content.
- Keep it lean: write a foundation card only when the concept is genuinely needed to follow the card. If a card
  stands on a concept that is itself niche (beyond a senior system-design round), say so in the ledger
  (`"note": "niche"`) instead of building a tower of prerequisites under it.
- Every fact you write is checked: numbers with `python3 -c`, product facts with a web search when unsure.

## Gate

`uv run python research/hello-interview/gen_skeleton.py` · `uv run trellis --domain hello-interview validate` 0 errors ·
`python3 -c` check that every folder you touched has steps 1..N exactly · the card checks in
`research/hello-interview/sdx/check_sdx.py` (`check_card`) pass for every card you wrote · `uv run python scripts/plain_style.py <new files>` ·
`python3 scripts/phone_diagrams.py <folder>` · `python3 research/domains/bagu/check_svg.py <folder>` lists none of your figures ·
`uv run python research/hello-interview/phrase_todo.py | tail -1` lists none of your files.

Reply in ≤ 6 lines: cards checked, foundation cards written (ids), concepts you judged niche, anything you were unsure of.
