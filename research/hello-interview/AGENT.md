# Card agent — Hello Interview deck (domain `hello-interview`)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, write only the cards of your
pages. Scratch in `/tmp/hi_<group>/`. `git checkout uv.lock` whenever uv touches it.

Chi (2026-11-01) is learning Hello Interview's system design and low-level design courses through this deck, in the
site's own order, before merging them into his `system-design` and `low-level-design` domains. **Resume rule:** skip a
page whose cards already exist.

## Input

Your pages are listed in your group file as leaf ids (`sd.<section>.<page>` / `lld.<section>.<page>`). The page text is
`sources/local/hello-interview/<track>__<section>__<page>.md` (the in-the-wild index is `system-design__in-the-wild.md`),
where `<track>` is `system-design` or `low-level-design`. Read the whole page first.

## The cards

Folder `vault/domains/hello-interview/cards/<sd|lld>/<section>/`, one file per card, frontmatter exactly:

```
---
id: hi-<sd|lld>-<page>-<n>-<short-slug>
node: <leaf id>
type: qa
step: <n>
---
```

- **Everything Chinese**, technical terms in English in parentheses on first use. Write in your own words — never copy
  sentences from the page (the site is commercial and the repo is public); facts, numbers and design choices are fine.
- **How many:** concept pages (core concepts, patterns, key technologies, in a hurry) 5–8 cards; problem breakdowns
  8–12; in-the-wild case studies 4–6; short overview pages 2–4. Cover what an interviewer probes, Pareto first.
- **Problem breakdowns** follow the site's delivery steps, one card each where the page has substance: functional and
  non-functional requirements (with the numbers), core entities and API, the high-level design's key flow, then one
  card per deep dive (the problem, the options the page weighs, the chosen one and why), and what is expected at
  mid / senior / staff level when the page says so.
- **Concept and technology cards:** the mechanism (why it works), the number or limit, the contrast with the nearest
  alternative, the failure or cost scenario, when to reach for it in an interview.
- **Low-level design breakdowns:** requirements, the classes and their responsibilities, the key method's logic in a
  short ```python block (type hints; comments carry the reasoning), and the extensibility follow-ups.
- Front: header `**<short title>**｜<track · section>` then a self-contained question (a reader with no page open must
  understand it). Back: label chips (`**要点。**`, `**为什么。**`, `**取舍。**`, `**数字。**`, `**易错。**` as fit), prose
  short — about 150–250 Chinese characters, a small table or ```svg diagram when it explains faster (phone width).
- No citations, URLs, "原文说", "Hello Interview 认为" or process talk on a card; the reading note links the page.

## Gate (before replying)

`uv run python scripts/plain_style.py <your files>` ok, `python3 scripts/phone_diagrams.py <your folder>` ok,
`uv run trellis --domain hello-interview validate` 0 errors and no `not_self_contained` / `leans_on_source` on your
cards. Reply in ≤ 6 lines: pages done, cards written, anything you were unsure of.
