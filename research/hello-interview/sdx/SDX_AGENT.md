# Merge agent: the System Design deck's cards into Hello Interview, without duplicates

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents. Scratch in `/tmp/sdx_<group>/`. `git checkout uv.lock`
whenever uv touches it. **Resume rule:** your ledger is the record; skip every SD card that already has a line in it.

Chi deleted the English `System Design` deck from Anki because he studies in Chinese. Its 856 cards (in
`vault/domains/system-design/cards/`) hold failure scenarios and details the other decks lack, and a lot they already
have. Your job, for the SD cards in your group: decide card by card whether a deck Chi studies already teaches it, and
turn what is missing into Chinese cards that pass the Hello Interview deck's standard. A duplicate costs him review
time every day for months; a missing point costs him a round. Both matter.

## Inputs

- `sources/local/hello-interview/sdx/groups/<G>.txt`: your SD card ids, ordered by SD leaf.
- `sources/local/hello-interview/sdx/candidates.json`: per SD card its `path`, its `home` (the Hello Interview leaf its
  new cards go to), `page_cards` (every existing card on that page), and the most similar existing cards: `hi_top`
  (Hello Interview cards and question bodies), `bagu_top` (八股), `pay_top` (支付系统核心), `other_top` (the HFT 低延迟交易系统,
  Kafka, 低层设计 and Snowflake decks, which Chi also studies). Similarity is lexical, so it misses paraphrases: also
  `grep -rl` the key terms (English and Chinese) in `vault/domains/{hello-interview,bagu,payments,hft,kafka,low-level-design,snowflake}/cards`
  and `vault/interviews/core/design-questions`. The English cdn-content and system-design decks do not count as coverage.
- `research/hello-interview/sdx/map.json`: SD leaf → home (for orientation; the home in candidates.json is the same).
- The model: `vault/domains/hello-interview/cards/premium/sdx/sd.problem-breakdowns.robinhood.more/hi-sdx-exchange-sequencer-journal.md`
  (two SD cards merged into one new card) and `sources/local/hello-interview/sdx/model_ledger.jsonl` (that merge plus two
  duplicates). Read both before you start.

## Per SD card

1. **Read it**, both the English (the original) and the `zh` translation (sometimes looser). A cloze card (`type: cloze`)
   has its text before the first heading and the Chinese under `## zh`; `{{c1::…}}` marks the tested part.
2. **Look for it.** Open the page cards' questions and the top candidates that look related; grep as above. Read the
   answers of the ones that might cover it.
3. **Verdict**, one line in `sources/local/hello-interview/sdx/ledger/<G>.jsonl` (append as you go):
   - `{"sd": id, "verdict": "dup", "covered_by": [paths], "why": "..."}`: an existing card teaches the same mechanism
     *and* its key reason or number. Several cards together may cover it; list them all. A card only in the System Design
     domain does not count.
   - `{"sd": id, "verdict": "new", "card": new_id, "fixed": "..."}`: not covered, or only partly: then the new card
     teaches the missing part, with just enough context to stand alone. Several SD cards on one point share one new card.
     `fixed` records anything you corrected (omit if nothing).
   - `{"sd": id, "verdict": "drop", "reason": "..."}`: trivia, outdated, or below what a senior candidate needs. At most
     20% of the group; never drop something because it is hard.
4. **Check before you write.** These SD cards were written without sources. Treat every claim as suspect: re-derive every
   number with `python3 -c`, check version-specific or product-specific facts (defaults, limits, which release) with a web
   search when unsure, and fix what is wrong. A plausible wrong card is worse than none.

## The new card (the deck's acceptance standard)

Folder `vault/domains/hello-interview/cards/premium/sdx/<home>/` (gitignored), file `<id>.md`, id `hi-sdx-<short-slug>`,
unique across all of `cards/premium/sdx/` (ls before choosing). Other groups may share a home folder: read what is
already there, never duplicate it, never edit another group's card.

```
---
id: hi-sdx-<short-slug>
node: <home>
type: qa
step: <n>
---
## Q
**<主题，≤ 20 字>**｜补充 · <页面中文名> · 必会|追问|加分

<the question as an interviewer asks it: a concrete situation, self-contained, no "in this design" without saying which>

## A
**结论。** <one or two sentences: the answer you would give first>

**要点。**
- **<短语 ≤ 12 字>：** <one or two sentences>
- ...

**为什么。** <the mechanism, plainly; optional if 要点 already carries it>

<optional figure or short code>

**面试里这样说。** 「<first person, 1–3 sentences, naming the exact value, key, structure or number>」

**易错。**
- **<短语>：** <the mistake and what it breaks>
```

- **Level:** 必会 = most rounds of this question reach it; 追问 = a senior follow-up; 加分 = beyond the bar. `step`
  orders the leaf: 必会 first, then 追问, then 加分; in a shared folder continue after the highest step already there.
- **One card tests one thing.** About 350 Chinese characters of answer, figures and code aside. Split rather than cram.
- **Self-contained:** no reference to other cards, decks, sources or "the original"; the page name in the title line
  gives the context.
- **Figures** when the point is a sequence, race, timeline, layout or structure: at least one new card in three. Rules
  as in `research/hello-interview/MOCK_AGENT.md` (```svg fence, width ≤ 340, theme variables, text fits its box, nothing
  overlaps; draw with a small checking helper, render at phone width on a dark background and look at it).
- **Code** only when the point is code (SQL, a Lua script, a command): ≤ 25 lines, comments explain it, prose does not
  repeat it.
- Chinese; English terms in parentheses on first use. No citations, no process talk. The checker rejects 原卡, 原文, 来源,
  本章, 本节, 这道题, 本题, 面经, 抓取 and similar.

## Gate (all must pass before you reply)

`python3 research/hello-interview/sdx/check_sdx.py <G>` 0 problems · `uv run python research/hello-interview/gen_skeleton.py` ·
`uv run trellis --domain hello-interview validate` 0 errors · `uv run python scripts/plain_style.py <your files>` ·
`python3 scripts/phone_diagrams.py <each of your folders>` · `python3 research/domains/bagu/check_svg.py <each folder>` lists
none of your figures · `uv run python research/hello-interview/phrase_todo.py | tail -1` lists none of your files.

Reply in ≤ 8 lines: dup / new / drop counts and new cards written; figures and how you checked them; what you fixed in
the SD content; the claims you are least sure of; any SD leaf whose home looks wrong.
