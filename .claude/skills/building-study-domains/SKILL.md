---
name: building-study-domains
description: Use when the user wants to learn a subject systematically or deeply (Kafka, Snowflake internals, a database, a protocol) as a trellis domain, add a new skeleton, or deepen an existing domain with cards, readings and drills.
---

# Building Study Domains

The goal is **retention**: fundamentals the learner can reproduce cold, months later, in an
interview or at work. Every step serves retrieval (cards), elaboration (drills and cases that
force producing the mechanism) and spacing (Anki and the pull → brief → grow loop). Vocabulary
is `CONTEXT.md`; the commands are `uv run trellis --domain <d> <cmd>`.

Keep `vault/<domain>/BUILD.md` as the durable record: the source survey, one ledger row per
finished step, and the next action. A new session resumes from it.

## Steps

1. **Survey the field, GitHub first.** Search curated material before anything else:
   `gh api -X GET search/repositories -f q="awesome <subject>"`, `"<subject> internals"`,
   `"<subject> interview questions"`. Then the canonical sources: official docs table of contents,
   the founding paper or book, engineering blogs, and existing interview kits in
   `vault/interviews/companies/*/`. Record each in `BUILD.md` with URL, licence and what it covers.
   *Done when* at least three independent outlines are listed, one of them official.

2. **Author the skeleton from the field** (ADR 0002) in `skeleton/<domain>.yaml`: the union of
   the surveyed outlines, never the learner's own topic list and never a codebase. A leaf is one
   interview probe. The learner reviews in Chinese: every new domain is `lang: zh`, with titles and
   summaries in Chinese and technical terms in English in parentheses, even when every source is
   English. Add a `requires` edge wherever understanding truly depends on another leaf
   (ADR 0005: a thin graph seals nothing). A free book may draft it: `trellis seed <corpus>` →
   `trellis accept`.
   *Done when* `validate` has 0 errors and every heading of every surveyed outline maps to a leaf
   or to an explicit out-of-scope line in `BUILD.md`.

3. **Ingest the corpus.** Declare each book, paper or doc set in `corpora/<id>.yaml`
   (`license: commercial` keeps text in gitignored `sources/local/`; free text uses `chapters:`
   URLs). Then `trellis ingest <id>` → `trellis triage <id> -o proposals/<id>.json` →
   `trellis accept proposals/<id>.json`.
   *Done when* every corpus is accepted and its unplaced sections are either new leaves or
   written down as gaps.

4. **Digest cards leaf by leaf.** `trellis digest <id> --next -o prompt.md` → answer as JSON →
   `trellis digest <id> --import answer.json --leaf <leaf>`. With helper agents, give each a
   disjoint leaf range and have it dedupe against existing card fronts. Card mix per leaf: the
   mechanism (why it works), the number or limit, the contrast with the nearest alternative, the
   failure scenario. Cards and reading bodies are written in Chinese. Leaves no corpus covers go
   through `trellis grow --leaf <domain>:<leaf>` → `grow --import` (scaffold carries no language rules).
   *Done when* `digest --status` shows every leaf done, `stats` shows no leaf without cards, and
   `validate` reports no `not_self_contained` or `leans_on_source` warnings.

5. **Add readings and archive them.** One readable, mechanism-level source per leaf, then
   `trellis clip`. *Done when* link coverage is ≥ 70% and no leaf lacks a readable source.

6. **Build the elaboration layer.** For each top-level node write a drill that makes the learner
   produce the mechanism: predict behaviour ("will this query prune?"), debug a symptom, or
   explain a design to a peer. Link drills to matching interview problems in
   `vault/interviews/` and to work Cases (skill `distilling-work-into-domains`).
   *Done when* every top-level node has at least one drill with grading points wikilinked to cards.

7. **Translate** only an older English domain being deepened (new domains are written in Chinese from step 2), following `docs/translation-spec.md`; audit
   a 10% sample by hand. *Done when* `validate` passes the bilingual cloze checks.

8. **Ship and start the loop.** `trellis sync` → `validate` → `build` → `anki-push` (desktop Anki
   running). Tell the learner the rhythm: daily review through the interleaved stream from
   `trellis feed`; weekly `trellis pull` → `trellis brief` → `trellis grow --next`. *Done when* the deck is in Anki and `BUILD.md` records the final
   `stats` line.

## Common mistakes

- Skeleton equals the topics the learner happened to name: the unknown unknowns never become leaves.
- Long explanatory notes instead of cards and drills: reading feels like learning and fades fastest.
- Cards that ask "what does chapter 3 say": they fail cold review and the `leans_on_source` lint.
- A dense domain with no `requires` edges: the feed shows advanced leaves before their foundations.
