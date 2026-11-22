---
name: building-study-domains
description: Use when the user wants to learn a subject systematically or deeply (Kafka, Snowflake internals, a database, a protocol) as a trellis domain, add a new skeleton, or deepen an existing domain with cards, readings and drills.
---

# Building Study Domains

The goal is **retention**: fundamentals the learner can reproduce cold, months later, in an
interview or at work. Every step serves retrieval (cards), elaboration (drills and cases that
force producing the mechanism) and spacing (Anki and the pull → brief → grow loop). Vocabulary
is `CONTEXT.md`; the commands are `uv run trellis --domain <d> <cmd>`.

**Everything the learner reads is Chinese**: skeleton titles and summaries, readings, cards,
drills. Technical terms stay English in full-width parentheses on first use, e.g.
微分区（micro-partition）. Sources may be English. `lang: zh` is the default; only an older English
domain says `lang: en`.

**Domains created after 2026-11-20** differ in three ways (Chi's rules, `AGENTS.md` § Deck rules): technical terms are
written in English as they are (prose stays Chinese); every card is self-contained in deck order (`terms.yaml` +
`scripts/term_order.py`); and a new subject is first tried as leaves of an existing deck (`research/domains/EXPANSION.md`)
— a new deck needs Chi's word. The flow that worked for seven domains: survey → `research/domains/<d>/outline.md`
(Chi reviews it) → `scripts/outline_to_skeleton.py` → 10–20 sample cards shown with `scripts/card_gallery.py` → card
agents on `research/agents/new-domains-cards.md`. A book Chi owns goes in `~/Books/` and is ingested as a `commercial`
corpus; plain PyMuPDF (the built-in pdf adapter) kept code indentation where Docling and PyMuPDF4LLM did not.

Put a new subject's content in `vault/domains/<domain>/` (skeleton `vault: domains/<domain>`) and keep
`vault/<folder>/BUILD.md` as the durable record: the source survey, one ledger row per
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
   interview probe. Add a `requires` edge wherever understanding truly depends on another leaf
   (ADR 0005: a thin graph seals nothing). A free book may draft it: `trellis seed <corpus>` →
   `trellis accept`. An agent may draft in English first; translate titles and summaries before
   step 3 and verify ids and `requires` are unchanged with a script.
   *Done when* `validate` has 0 errors and every heading of every surveyed outline maps to a leaf
   or to an explicit out-of-scope line in `BUILD.md`.

3. **Ingest the corpus.** Declare each source in `corpora/<id>.yaml`: a paid book is
   `license: commercial` with `file:` (text stays in gitignored `sources/local/`); free text,
   including vendor docs published free online, is `license: free-online` with `chapters:` URLs
   (check each URL returns 200 first). Then
   `uv run --extra clip trellis ingest <id>` (the extra is required for URLs; `--retry` after a
   failure) → `trellis triage <id> -o <prompt>` → an agent writes `proposals/<id>.json` →
   `trellis accept proposals/<id>.json`. Reading bodies follow the domain's language.
   *Done when* every corpus is accepted, its gap verdicts are written in `BUILD.md`, and the list
   of leaves with no reading is recorded there.

4. **Cards, leaf by leaf.** Card mix per leaf, 4–6 cards: the mechanism (why it works), the number
   or limit, the contrast with the nearest alternative, the failure or cost scenario.
   - Leaf with a corpus section: `trellis digest <id> --leaf <leaf> -n 5 -o prompt.md` → JSON →
     `trellis digest <id> --import answer.json --leaf <leaf>`.
   - Leaf without one: `trellis grow --leaf <domain>:<leaf> -o prompt.md` → JSON →
     `trellis grow --import answer.json --leaf <domain>:<leaf>` (scaffold carries no language rules).
   - Orchestration: see **Card agents** below.
   - Diagrams: at least 25% of the domain's cards carry a ```mermaid block or a bare `<svg>` block (never fenced, so
     Obsidian draws it), aim 30%; check with
     `uv run python scripts/diagram_share.py <domain>`.
   *Done when* `stats` shows every leaf with cards and `validate` reports 0 errors and no
   `not_self_contained` or `leans_on_source` warnings.

5. **Review grown cards.** Cards written by `grow` have no source behind them. Ask each card agent
   to list the claims it is least sure of; put that list in `BUILD.md` and give those leaves a
   readable source in step 6 first. *Done when* every listed claim is checked against a source or
   the card is rewritten.

6. **Add readings and archive them.** One readable, mechanism-level source per leaf, then
   `trellis clip`. *Done when* link coverage is ≥ 70% and no leaf lacks a readable source.

7. **Build the elaboration layer.** For each top-level node write a drill that makes the learner
   produce the mechanism: predict behaviour ("will this query prune?"), debug a symptom, or
   explain a design to a peer. Link drills to matching interview problems in
   `vault/interviews/` and to work cases (skill `distilling-work-into-domains`).
   *Done when* every top-level node has at least one drill with grading points wikilinked to cards.

8. **Ship and start the loop.** `trellis --all sync` → `--all validate` → `--all build` (no
   `--lang`: a Chinese domain refuses it) → `--all anki-push` (desktop Anki with AnkiConnect on
   :8765). Tell the learner the rhythm: daily review through `trellis feed`; weekly
   `trellis pull` → `trellis brief` → `trellis grow --next`. *Done when* the deck shows in Anki and
   `BUILD.md` records the final `stats` line.
   A new domain alone: `uv run python scripts/anki_refresh.py --dry-run --add <id-prefix> <domain>` (the count must
   equal the new cards), the same without `--dry-run`, then `uv run trellis --domain <domain> anki-align` to put its
   decks on their own preset. This keeps the `Note` fields and touches no other deck. Sync before and after.

An older English domain being deepened adds translations instead of rewriting: follow
`docs/translation-spec.md` and audit a 10% sample by hand.

A domain whose interview form is *problems* (design X, implement Y) gets a problem bank on top of its concept
leaves: skill `building-problem-banks`. An article written in the vault is a reading with no `url:` — it needs no
clipping and card footers open it; a reading tagged `no-archive` keeps its link and is never clipped.

## Card agents

- Split the leaves by top-level node into up to 3 disjoint groups; one agent per group owns
  `vault/<folder>/cards/<node>/` for its nodes and nothing else.
- Write one prompt template to a file (paths, both import paths, card mix, language, gate) and
  render it per group; each agent reads its file. Shell steps inside agents are plain single commands.
- Every prompt starts with a resume rule: check `stats` and the cards folder, skip leaves that
  already have cards. A usage-limit death then costs nothing: commit what validates, relaunch.
- Subagents default to `sonnet`; when sonnet hits its session limit, relaunch on `opus`.
- Accept a group only after running `validate` and `stats` yourself and reading at least one card;
  commit per group, staging only that group's card folders.
- Web research has two limits the agents share. All agents of one turn draw on one pool of 200 web searches, and
  five research-heavy agents in parallel used up the account's usage window in about 20 minutes (twice). Put a search
  budget in the brief (at most 3 searches a card, fetch the abstract page by URL instead), have each agent write its
  file and its ledger row card by card, and commit what exists after every interruption. Three agents is the rule;
  more only when Chi asks.
- Review the first wave before launching the next and add what you found to the brief as rules: the later waves then
  need almost no fixes.
- Leaves in different groups that share one source page produce duplicate cards: after the last
  group, list the questions of every such leaf pair and delete the duplicates from one side.

## A domain of research findings (psychology, economics, health)

Model: `psych` (`research/domains/psych/`: `BUILD.md`, `CARDS_TASK.md`, `tree.txt`, `gen_tree.py`, `review.py`).
What differs from a technical domain:

- **The tree lives in one text file with an anchor per leaf.** `tree.txt` holds every leaf's title, summary, evidence
  grade and *anchor* (the studies and numbers to start from, written from memory and treated as unverified). A script
  turns it into the skeleton, the per-group anchor lists and the full map note. List every concept of the field; mark
  the first wave `core: true` and leave the rest as leaves without cards.
- **Grade the evidence on the card.** A: replicated or meta-analytic. B: small, conditional or thinly replicated.
  C: famous and failed. Give the failed classics their own cards; a deck that only lists effects teaches the wrong ones.
- **One card per concept, story first.** Situation question → one bold sentence → `**故事。**` one real event with
  names, year and numbers → evidence line with the grade → who uses it (only when documented) → an action with a
  trigger. The original experiment is usually the best story.
- **Every number is checked this session, and the check is logged.** The agent confirms each number against the paper
  or two reliable summaries and appends a row to `claims-<group>.md` (claim, URL, what differs from the anchor). A
  number it cannot confirm stays off the card. In `psych` this caught about one anchor error in ten and lowered nine
  grades; memory alone would have shipped them.
- **Review by reading, with a script for the rest.** `review.py` checks layout, tags against the tree, length, banned
  phrases and figure share; `--dump <group>` prints only the cards not yet read. Then read all of them: look for a
  median written as a mean, a percentage change written as percentage points, an action nobody could carry out, a
  question whose own numbers do not add up, and a story that only narrates the paper. Sync the grades the agents
  changed back into the tree.
- **The generated tree note shows only carded leaves** (`scripts/knowledge_tree.py` skips a node with no cards). When
  the field's whole map matters, write a second note from the tree file with the uncarded leaves marked.

## Common mistakes

- Skeleton equals the topics the learner happened to name: the unknown unknowns never become leaves.
- A skeleton without `lang` in an old checkout, or an English triage prompt: the whole deck comes out English.
- Long explanatory notes instead of cards and drills: reading feels like learning and fades fastest.
- Cards that ask "what does chapter 3 say": they fail cold review and the `leans_on_source` lint.
- Grown cards shipped unreviewed: plausible, confident and occasionally wrong.
- A dense domain with no `requires` edges: the feed shows advanced leaves before their foundations.
- A deck Chi cannot read on the phone: he studies in Chinese. A domain written in English needs `## zh` translations
  and `show: zh`, and Chinese node titles 「中文（English）」.
- AI or ML material that assumes background: open with the basics, define every term on first use, keep a strict
  reading order (`requires`), and model it on `llm-inference:basics`.
- Fewer than 25% of cards with a diagram, or svg fenced as ```svg (Obsidian shows it as code).
- Several decks holding copies of one item: one source, one card; lists and companies are tags (see
  docs/explanation/study-system.md).
- A number, a quote or an anecdote on a card that nobody looked up this session. Unconfirmed means left out.
- A card of findings with no size on it: say how big the effect is and whether it replicated.
