# Trellis

Skeleton-constrained knowledge base. One YAML mind map defines the topics, their
study order, and their prerequisite edges. Two kinds of content attach to its
nodes, both plain Obsidian markdown:

- **Cases** — decisions taken from a real codebase, rewritten in a lens's
  vocabulary and attached to the leaf whose principle they instantiate. Evidence
  for cards, never cards themselves. See [Studying a codebase](#studying-a-codebase).
- **Cards** — atomic Q&A / cloze fragments for spare-time review; the build
  compiles them into an Anki `.apkg` you can re-import forever without duplicates.
- **Readings** — long-form, authoritative material (papers, engineering-blog
  essays, book chapters) for systematic study; a reading can span several nodes.
- **Drills** — output practice: design questions and exercises with constraints,
  grading points, and an attempt log. Cards recall, readings feed in, drills
  train the 40-minute performance.

Cards and readings reference each other with ordinary wikilinks, and every node's
generated map note lists both — so the Obsidian graph connects topic ↔ reading ↔
card.

Ships with nine domains (seven fully carded, plus Markets & Factors and Quant
Infrastructure as skeleton + readings). **CDN Content** — a 75-node map
(198 bilingual cards, 52 readings, 4 drills) for serving content at the edge:
the request path, HTTP, caching semantics, Go/Node/OpenResty runtimes, the
content lifecycle from SSG to ISR, distributed architecture, reliability,
safe delivery, and security and cost. **Stripe** — the online assessment as
eleven probe groups in Chinese (40 cards), with the study handouts and one
question/solution pair per problem beside them; the raw research behind it
(catalog, rounds, reports) is archived as plain notes under
`vault/interviews/companies/stripe/`. **Kafka** — a 79-node map in Chinese
(340 cards, 88 readings) digested end to end from Kafka权威指南（第2版）with
the flow under [Digesting a corpus](#digesting-a-corpus): ingest the epub,
seed the skeleton from its outline, triage 140 sections onto 66 leaves, write
cards leaf by leaf from the text, and read back what the book never reached.
**System Design** — a 100-node map
(465 cards, 81 readings) structured against DDIA 2nd edition and spanning the interview canon
plus what the 2017-era resources miss: consensus, CRDTs, encoding and schema
evolution, delivery semantics, idempotency/outbox/saga/ledger, OLAP and
lakehouse, SLOs, multi-region, AI serving. **Low-Level Design** — a 33-node map
(125 cards) covering the machine-coding round: object modelling, SOLID as
refactoring triggers, the GoF catalogue by intent, code smells, concurrency,
and program structure. **Code Core** — an 86-node map (379 cards, 35 readings,
9 drills) for the timed coding round that is not LeetCode: reading a multi-part
spec, parsing stdin into records, modelling state that survives a reversal,
money and threshold arithmetic, time and intervals, byte-exact output, the
data-structure and algorithm toolbox, complexity budgets, language fluency,
correctness discipline, and how the same core transfers to another company's
assessment. **Basketball** — an 86-node map (161 cards, 24 readings, 5 drills)
for the advanced amateur: the geometry of advantage and spacing, one-on-one,
the two-man game, team offense, the named systems (motion, Princeton,
triangle, five-out), all eleven defensive leaves from closeout to pick-and-roll
coverage to the rotation that actually breaks, the reads that make up
basketball IQ, special situations, analytics you can play with, physical
preparation, practice design, and the rules that change decisions. Every leaf
in those four is covered; Kafka's four empty leaves are the ones the book
does not teach, listed in its Corpus note as the reading list.

That last domain is why a **video** is a first-class source: tag a reading
`video` and it counts as readable without being clipped — a watch page
archives as navigation chrome, never content — ranks beside archived prose,
and its card footer link goes straight to the footage, marked ▶ so you know
what a tap will do. A subject learned by watching is now as well-served as
one learned by reading.

## Why a skeleton

Every existing markdown→Anki tool treats cards as a flat bag. Trellis inverts
that: the skeleton is the source of truth, and everything is derived from it —

- **Anki deck hierarchy and ordering** (`System Design::06 Distributed Data::Consensus`)
  follow the map, so new cards always arrive in prerequisite order.
- **Obsidian graph** mirrors the map: `trellis sync` generates one linked note
  per node (breadcrumbs, prerequisites, what each topic unlocks, its cards).
- **LLM generation is fenced in**: prompts are scaffolded per-node with the
  node's scope, siblings marked out-of-scope, and existing cards to avoid
  duplicating; the LLM's JSON is validated against the skeleton before a single
  file is written.
- **Validation is structural**: a card pointing at a dead topic, a duplicate id,
  or an uncovered leaf is a build error or warning, not silent rot.

## Quickstart

```bash
pip install -e .
trellis validate          # skeleton + cards/readings/drills, structural checks
trellis build             # -> dist/system-design.apkg, import into Anki
trellis sync              # regenerate Obsidian map notes
trellis path --weeks 8    # write a week-by-week study plan into the vault
trellis stats             # coverage per branch
```

Validation also guarantees the study order is coherent: a node can never
appear before one of its `requires` prerequisites — tree order in the
skeleton is checked against the edges.

## Links are the product

The vault is meant to be the definitive index: for every topic, the one
authoritative, approachable resource — so studying never starts with a search.
Mechanically:

- Readings with a `url` become a clickable **"Go deeper"** footer on every Anki
  card under their node (ancestors included — a branch-level reading covers the
  whole branch).
- `trellis stats` reports **link coverage** (cards with a road onward) per
  branch; `trellis validate` warns when a domain drops below the 70% target.
- A source only counts as **readable** when it is archived in the vault, has
  real prose, and is not tagged `book` or `index`. Preference order, highest
  first: an engineering-blog deep dive, a company write-up, a paper, or a
  single section of a knowledge base — then anything else on the web — then
  books and indexes, which rank last however cleanly their homepage happens to
  archive. Tag a genuine full chapter `canonical`, not `book`. `validate`
  names every leaf still stuck with a pointer, so this cannot regress quietly.
- `python3 scripts/check_links.py` verifies every archived URL still resolves
  (run manually; network-bound).

### One app to read in

A reading is a pointer; a **clipping** is the page itself, saved as markdown in
the vault. Every card's footer links to its reading note with
`obsidian://open?...` — tapping it in Anki opens that note *in Obsidian*, where
`trellis sync` has embedded the clipped article, so you read with your own
typography, highlights and backlinks, online or not. The web original stays one
↗ away. See [ADR 0001](docs/adr/0001-obsidian-as-the-reader.md).

Links name the note rather than its path, so the same card works on a laptop
whose vault root is `vault/` and a phone whose git client cloned the whole
repo. That requires unique names, which is why clippings are stored as
`<reading>-clip`.

```bash
trellis --all clip          # fetch every unclipped reading into vault/<folder>/clippings/
trellis --all build         # footers now point at the local copies
```

Clippings are matched to readings by URL — the same `source:` property
[Obsidian Web Clipper](https://obsidian.md/clipper) writes — so anything you clip
by hand with the extension (point it at `<domain>/clippings/`) is picked up
identically. Pages that are the resource itself (videos) or that hide behind
JavaScript are skipped with a reason and stay web links.

Clippings **are committed**, because this repository is private and a clone is
how the archive reaches a phone. They remain other people's writing: making the
repository public again means removing them first (`git rm -r --cached
vault/*/clippings` and restoring the ignore rule that is kept, commented, in
`.gitignore`). They are reproducible either way — `trellis clip` rebuilds them
anywhere.

- **Anki**: import `dist/system-design.apkg`. After editing or adding cards,
  rebuild and re-import — note GUIDs are stable, so edits update in place and
  your review history survives.
- **After a skeleton restructure** (renamed/split/reordered nodes): Anki never
  moves existing cards between decks on import, so stale deck names linger with
  the old cards inside. Fix in one step on desktop Anki (with the
  [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed):
  import the new `.apkg` first, then `trellis anki-align`, then sync to
  AnkiWeb. Cards are matched by their stable node tags, moved to the decks the
  current skeleton defines, and emptied stale decks are deleted. Top-level
  branches carry an explicit `order:` in the skeleton, so their deck numbers
  never shift when new branches are inserted.

### Publishing to the phone

`build` produces a file; `anki-push` is that file reaching the phone. It runs
the four steps in the order that makes them safe, against desktop Anki with the
[AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on:

```bash
trellis --domain system-design anki-push --lang zh
#   built 391 notes in 71 decks
#   pulled from AnkiWeb        <- the phone's reviews land first
#   imported system-design.zh.apkg
#   moved 12 card(s), removed 2 stale deck(s)
#   pushed to AnkiWeb          <- the phone gets the new cards
```

It builds the package itself rather than trusting whatever sits in `dist/`,
because **Anki updates a note only when the incoming one is newer**. Re-importing
a package built before the collection last changed leaves those notes silently
stale — which is exactly what happens when you switch languages and push the old
file again. Building inside the command removes the trap.

Switching language is a push, not a migration: card ids and therefore note GUIDs
do not depend on language, so `anki-push --lang zh` rewrites the text of the
cards already in the collection and every review history survives.

Syncing **before** the import is the point: it puts the package on top of
current scheduling rather than a stale collection, so nothing reviewed on the
phone is lost. Aligning between import and the final sync means decks renamed or
split since the last push are reconciled in the same trip.

### The order and the mix Anki deals

Anki shows new cards by a *position* each one carries, and its importer never
moves a card it already has — so until the vault decides that number and keeps
deciding it, nothing you reorder is ever seen on the phone
([ADR 0010](docs/adr/0010-the-vault-decides-the-order-and-the-mix-anki-deals.md)).

```yaml
# skeleton/kafka.yaml
study:
  order: core-first        # the Core, then the rest — or `skeleton` for plain tree order
  mix: new-first           # new-first | mixed | reviews-first
  new_per_day: 20
  reviews_per_day: 100     # half and half is equal limits with `mix: mixed`
nodes:
  - id: core
    core: true             # on a branch it covers the subtree
```

```markdown
---
id: kafka-core-offset-what-is
node: core.offsets
step: 1                    # met first among this leaf's cards
---
```

- The **Core** is what you declare plus everything it requires, so the first pass
  never meets a card before its ground. With nothing declared, the leaves
  something else stands on are the Core.
- A **step** orders cards inside a leaf; unstepped cards follow, grown cards come
  last. `trellis --domain kafka steps -o prompt.md` asks a Runner for the order
  of every leaf, and `steps --import answer.json` lands it as one frontmatter
  line per card (`--check` validates without writing).
- `anki-push` numbers the package in that **Sequence**, then converges the
  collection: every card Anki still calls *new* gets its position; a card with a
  review history is never touched. `anki-align` does the same without importing.
- The domain's decks move to a preset of their own, `Trellis · <title>`, cloned
  from what they used and set to deal new cards by position — without it sibling
  decks are dealt alphabetically. The **Pace** lands there too. The preset the
  rest of your collection shares is never written to.
- Core cards carry `trellis::core`, so `tag:trellis::core is:new` is a filtered
  deck of exactly the first pass. The Study Path and every map note list in the
  same order.

One manual step: with a review backlog at or above `reviews_per_day`, Anki's v3
scheduler shows no new cards unless *Deck options → New cards ignore review
limit* is on. That switch is collection-wide and AnkiConnect cannot reach it.

### Granularity policy

A leaf is **one interview probe** — a topic narrow enough that "I'm weak here"
points at something specific to drill or generate more cards for. Split a leaf
when it accumulates more than ~6 cards or you can't name the single skill it
trains. Splits are cheap: edit the skeleton, re-point the affected cards'
`node:` lines, `trellis sync && trellis build`, and `trellis anki-align` makes
the live collection follow.
- **Obsidian**: open `vault/` as the vault (not a single domain folder), so
  wikilinks work across domains. Each domain's `map/` holds the generated topic
  notes (your own text outside the `%% trellis %%` markers is preserved). The
  graph view is the mind map.

## Languages

A domain is written in the language you study it in — `lang: zh` in its
skeleton, and every card's `## Q`/`## A` is simply in that language. There is
no English original to keep: a domain digested from a Chinese book is
Chinese, and its deck is Chinese with nothing else. Terms of art stay English
in any language (`consumer group（消费者群组）`), because that is how the
reader will meet them in code and docs.

A domain written in English may carry a translation, **appended**, never
substituted, so nothing is lost if one is wrong or missing:

```markdown
## Q
A hot key expires and 10k requests hit the database at once…

## A
**Cache stampede.** Request coalescing, or jittered TTLs…

## Q zh
一个热点 key 过期，1 万个请求同时打到数据库……

## A zh
**缓存击穿（cache stampede）。** 请求合并，或给 TTL 加抖动……
```

A cloze card takes a single `## zh` section instead, with its `{{c1::…}}`
deletions kept byte-identical — the deletion is the answer being tested.

```bash
trellis build --lang zh     # cards render in Chinese where a translation exists
```

**Switching language is not a new deck.** Card ids — and therefore Anki note
GUIDs — do not depend on language, so re-importing a translated build swaps the
text in place and your review history survives. Technical terms stay in English
by policy; see [the translation spec](docs/translation-spec.md). `trellis stats`
reports translation coverage per language.

## Card format

One file per card under `vault/<folder>/cards/<branch>/`, filename = card id:

```markdown
---
id: caching-stampede-protection
node: caching.invalidation
type: qa            # qa | cloze
---
## Q
A hot key expires and 10k requests hit the database at once. Name the failure
and two mitigations.

## A
**Cache stampede.** Request coalescing (one recomputes, rest wait) or
jittered/early refresh so keys never expire under full load.
```

Cloze cards drop the Q/A sections and use Anki syntax in the body:
`{{c1::W + R > N}}`. Wikilinks are allowed and render as styled plain text in
Anki.

## Reading format

One file per reading under `vault/<folder>/readings/`; `nodes` may list several
topics:

```markdown
---
nodes: [async.log, async.streaming]
url: https://engineering.linkedin.com/...
---
# The Log: What every software engineer should know
Why read, what to extract, and wikilinks to related cards.
```

## Growing content with an LLM

```bash
trellis scaffold distributed.consensus -n 8   # emit a fenced, context-rich prompt
# paste into any LLM, save its JSON answer:
trellis import batch.json                     # all-or-nothing validation, then files
trellis sync && trellis build
```

## Digesting a corpus

A **corpus** is one body of material with an outline of its own — a book as
an epub or a pdf, a freely published one as chapter URLs, a markdown file
you converted by hand. It is declared, like a codebase:

```yaml
# corpora/kafka-2e.yaml
title: Kafka权威指南（第2版）
license: commercial            # decides where the text may live
domain: kafka                  # the skeleton it lands on — seeded if absent
lang: zh                       # cards are written in the book's language
home: https://www.ituring.com.cn/book/2937
file: ~/Books/kafka-2e.epub    # or  chapters: [https://…, …]  for a free book
```

```bash
trellis ingest kafka-2e          # sections + outline (pdf needs pip install -e '.[ingest]')
trellis seed kafka-2e            # no skeleton/kafka.yaml yet: draft one from the outline
trellis accept proposals/kafka-2e.seed.json
trellis triage kafka-2e          # every section beside every leaf -> a proposal
trellis accept proposals/kafka-2e.json        # readings with provenance, gaps listed
trellis digest kafka-2e --status              # leaves the book reaches: todo / done
trellis digest kafka-2e --next -o prompt.md   # the next leaf, grounded in its sections
trellis digest kafka-2e --import cards.json --leaf producer.acks
trellis --domain kafka sync && trellis --domain kafka build --corpus kafka-2e
```

Every step that involves an LLM has the same shape: a prompt out, JSON back,
validated all-or-nothing before a file is written. The LLM never touches the
vault. Who answers the prompt is up to you — a chat window, or agents
digesting disjoint leaves in parallel: nothing is recorded that can be
derived, so `--status` is read off the vault (readings carrying `corpus:`,
cards carrying `source:`) and parallel writers share no state file.

**Where the text lives** is decided by the license. Freely published
material archives into `sources/archive/<id>/` and is committed; sections a
triage accepts get clipped beside their readings like any web article. A
book you paid for is ingested into `sources/local/<id>/`, which git ignores:
the text is needed on this machine to triage and digest, and nowhere else.
Its outline — titles only — is committed either way, so the Corpus note and
`digest --status` work everywhere. Web chapters checkpoint per fetch in
`pipeline/state/ingest-<id>.json`; re-running resumes, `--retry` re-attempts
failures.

**The book's structure is not the skeleton.** Its outline stays its own
thing, and the two are related only by triage, section by leaf. What the
book never reaches is the most useful output: `vault/Corpora/<id>.md` shows
the outline annotated with what each section became, and underneath it the
leaves of the domain the book does not teach — your reading list. A subject
with no skeleton may be *seeded* from a canonical book's outline, judged as
a map of the field with the leaves the book omits added by that review; see
[ADR 0006](docs/adr/0006-a-corpus-enters-as-readings-and-may-seed-a-skeleton.md).

**A deck for the book is a filter.** `build --corpus <id>` writes the subset
of the domain's cards written from it, with the same ids and therefore the
same Anki note GUIDs — never a second deck. Every card from a corpus also
carries the tag `src::<id>`, so a filtered deck inside Anki does the same.

**Cards written from a book must teach without it.** The digest prompt says
so in as many words: the question carries its own situation, the answer
defines every term it uses and says why, and "as discussed in chapter 3" is
forbidden. A reader who has never opened the book must understand the card
from the card alone.

## Drill format

One file per drill under `vault/<folder>/drills/`; same frontmatter as
readings (`nodes` lists every topic the exercise exercises). Body: prompt,
constraints, grading points, attempt log. Node map notes list their drills.

## Studying a codebase

A repository can be ingested as a learning target. It is *declared*, not
discovered — the sharpest decisions in a real codebase are rarely where a
heuristic would look (in the first one ingested, nine architecture rules with
their rationale live in a lint config):

```yaml
# codebases/quant-stroller.yaml
repo: ChiChasesCheese/Quant-Stroller
ref: main
harvest:
  - path: .importlinter        # architecture rules -> Case
    kind: contracts
  - path: docs/adr/*.md        # decision records  -> Case
    kind: decisions
  - path: docs/concepts/*.md   # subject matter    -> reading + clipping
    kind: subject
    lens: quant-infra
```

```bash
trellis triage quant-stroller --kinds decisions,contracts --lens system-design,low-level-design
# hand proposals/quant-stroller.prompt.md to an LLM, save its JSON answer
trellis accept proposals/quant-stroller.json
```

`triage` shallow-clones into a gitignored cache, pins the commit, and writes a
prompt listing every artefact beside every leaf it could attach to. The LLM
answers with a proposal; `accept` validates it against the skeletons and writes
files all-or-nothing — the LLM never touches the vault.

**A decision becomes a [Case](CONTEXT.md)**: rewritten in the lens's vocabulary,
attached to the leaf whose principle it instantiates, frozen at the commit it
was read from. Cases are evidence for cards, never cards themselves — a card
asking "what did we decide about X" tests recall of your own conclusion and is
worthless in an interview.

**An artefact that fits no leaf is a `gap`**, not an error: it proposes growing
the skeleton. That is why skeletons are authored from the field first and
codebases are mapped onto them afterwards — see
[ADR 0002](docs/adr/0002-skeletons-are-authored-from-the-field.md) and
[ADR 0003](docs/adr/0003-a-codebase-enters-as-cases-and-subject-material.md).

## The loop

Everything above flows one way: a skeleton decides, content hangs off it, a
deck is built. The way back is `pull` → `brief`.

```bash
trellis --all pull          # read the review history out of Anki into traces/
trellis brief               # write vault/Brief.md: what to do next
trellis feed                # the filtered-deck recipe for spare minutes
```

`pull` is the only command that asks Anki a question. It writes
`traces/<domain>.json` and stops; everything downstream reads that file, so the
Brief regenerates on a phone that cloned the repo, in CI, and with Anki closed
([ADR 0004](docs/adr/0004-traces-are-pulled-into-a-file-the-repo-owns.md)).
Notes are matched back to cards by an `id::<card-id>` tag the build now writes —
a note GUID is a hash and cannot be reversed, a tag can. Cards imported before
that tag existed are counted and named; one `anki-push` repairs them.

Four things are then computed from the Traces, and they are the vocabulary the
Brief speaks in:

- **Hold** — how well a node is retained, read off the interval the scheduler
  already trusts and normalised against Anki's own 21-day maturity bar. A curve,
  not a badge: nothing changes discontinuously as a card crosses a threshold.
- **Bearing** — how much of the skeleton rests on a node, from the transitive
  `requires` graph. High bearing × low hold is what to repair first; that is the
  80/20, computed rather than asserted.
- **Sealed** — a leaf whose prerequisites are not holding. Its cards are
  withheld from the Feed until the ground under them takes
  ([ADR 0005](docs/adr/0005-a-leaf-is-sealed-until-its-prerequisites-hold.md)).
- **Uncovered** — a leaf with no cards. Nothing to fail, so it wants writing,
  not practice. That is the distinction `trellis brief` exists to keep straight.

Thin evidence is shrunk toward the branch it hangs from, so one unlucky card
cannot shout as loud as forty measured ones — and a leaf nobody has reviewed is
reported as unproven rather than weak. "No data", "not enough data" and "really
weak" are three different situations wanting three different actions.

A new card is "not enough data" too. Hold reads the interval, and a card first
shown yesterday has a one-day interval however well it was answered — so each
card gets a **verdict** (unseen, young, taken, slipped) and only the last two
count. Without this, 70 of the 71 leaves the loop called weak on the real
collection were simply in their first week
([ADR 0009](docs/adr/0009-the-loop-waits-for-a-verdict-before-it-acts-again.md)).

There is exactly **one Brief and it spans every domain**, with a cap on how many
rows any one domain may take. A per-domain report would be a better dashboard
and a worse instrument: it would let you sink into the subject you are already
best at.

### The Feed

The deck tree is how you author. It is a bad way to review in the four minutes
before a train arrives, because it makes you choose a deck before you have
learned anything. `trellis feed` prints the search for one Anki **filtered
deck** spanning every domain, in random order, with sealed leaves held back —
one stream, no decision, and consecutive cards from different subjects.

That last property is the point twice over: mixing topics is what makes a feed
hold attention, and interleaving is also what makes retrieval practice stick
better than blocking it. A filtered deck rather than a new app because a note
lives in exactly one deck — this keeps one scheduler and one review history.

### Grow: the verdicts become cards

The Brief names a weak leaf or an empty one; `trellis grow` is what happens
next, and it closes the loop: review → Trace → Brief → new cards → review.

```bash
trellis grow                              # the weak and uncovered leaves, what each can be written from
trellis grow --next -o prompt.md          # a prompt for the top one
trellis grow --leaf kafka:producer.acks -o prompt.md
trellis grow --import answer.json --leaf kafka:producer.acks
```

The two kinds of target get two different prompts. A **Weakness** already
has cards and they slipped, so the prompt carries the ones that lapsed
most — front and back — and asks for cards that reach the same mechanism
from *another angle*: a scenario, a contrast, a failure story, a number.
Restating a card that already failed teaches the same failure twice. An
**uncovered** leaf gets the scaffold's prompt, grounded in whatever the
vault already holds for it: the sections of a corpus that reaches the leaf
(then growing is digesting, and the cards carry the corpus as `source:`)
or the clipped readings on it. Either way the answer lands through the same
importer as every other card — forced onto the leaf, refused if it leans on
its source — and is tagged `grown`. `grow` only writes where the loop pointed;
anywhere else is `scaffold` or `digest`.

The tag is how the loop remembers having acted. The grown cards on a leaf are
its **Graft**: *settling* until enough of them have been reviewed to judge, then
*took* or *slipped*. While a Weakness's Graft is settling the evidence is the
same evidence, so `grow` leaves it alone, and the Brief opens with **先复习**
and the Anki search for exactly those cards instead of asking for more. Once
they are reviewed the Brief reports the result under **新卡**; a Graft that
slipped puts the leaf back, and the next prompt shows the grown cards that
failed beside the originals so the third route differs from both. The whole
circle — push, review, pull, brief, grow, push, review, pull — runs in
`tests/test_loop_e2e.py` against a fake Anki that imports the real `.apkg`.

### The Workbench

```bash
trellis serve                # http://127.0.0.1:8777 — opens in the browser
```

The loop as a page, in Chinese, served from the repository on this machine
and doing only what the commands above do (ADR 0007). The left rail lists
every domain with its Hold; the page is one domain at a time. Its centre is
the **lattice**: one row per branch, one cell per leaf, the cell's green the
leaf's Hold, hollow when the leaf has no cards, hatched when it is sealed.
Click a cell or a row in *该修的* / *该写的* and a drawer opens with the leaf's
standing, the cards held least, what there is to read and practise, and four
actions: open the map note in Obsidian, open the leaf's cards in the Anki
browser, make them due today (Focus), or review the deck. Below the lattice:
the Hold trend over past pulls (from `traces/`' git history), the Brief, and
the grow log.

Growing from the page is the same `grow` as on the command line with one
addition, **Guidance**: a text box for what to emphasise or which angle to
take, appended to the prompt. The answer comes from Claude Code on this
machine (`claude -p`, the Runner) and is shown for review; *写入* lands it
through the same importer as everything else, *写入并推到 Anki* also builds and
publishes. Jobs live under `.trellis/jobs/` so a reload keeps them.

### Adopting a deck that lives only in Anki

```bash
trellis adopt leetcode --anki "LeetCode"        # 1: writes the seed prompt from the deck's inventory
trellis accept proposals/leetcode.seed.json     # 2: the drafted skeleton
trellis adopt leetcode --anki "LeetCode"        # 3: mirrors every note onto its leaf, tags it in Anki
trellis --domain leetcode pull                  # its reviews now reach the loop
```

A deck another tool wrote straight into Anki — no markdown anywhere — can
still stand on a skeleton. Each note becomes an **adopted card**: `anki:
<noteId>` in its frontmatter, placed on the leaf whose id ends in the concept
the note is tagged with (a question's concept-less notes borrow the concept
their siblings carry; the rest fall back to the note's most specific topic),
and tagged in Anki with the id and node Trellis knows it by. Adopted cards
are read for their Traces and grown beside; `build` skips them and `align`
leaves a note tagged `trellis::adopted` where its owner put it. Re-running
step 3 refreshes the mirrors.

### Content made somewhere else

Domains are discovered from `skeleton/*.yaml`, so a folder of perfectly good
cards written on another machine is invisible to every command. `trellis adopt`
fixes that: it reads the `node:` lines the cards already carry, rebuilds the
tree those dotted ids imply, and writes the skeleton that was latent in them.

```bash
trellis adopt                      # list vault folders no skeleton claims
trellis adopt stripe               # write skeleton/stripe.yaml from their node ids
trellis --domain stripe validate
```

Nothing is invented — every node is a prefix of an id some real card claimed,
and titles come from the map notes when they exist. What it cannot recover is
study order, because that is not in a pile of cards; children come out sorted
and the file header says so. Reordering them, adding `summary:` lines and adding
`requires:` edges are the three edits that turn a valid skeleton into a useful
one.

`validate` also now checks that cards are **self-contained** — no question
opening on a pronoun with no antecedent, no pointing at another card, no answer
so long it is testing three things. Those rules are narrow on purpose (each was
checked against the whole collection and anything producing a false positive was
dropped), and their real job is guarding this way in: imported cards never
passed through the scaffold prompt that asks for atomicity.

## Adding a domain

Drop `skeleton/<domain>.yaml` (same shape as `system-design.yaml`), set `vault:` to
the folder its content lives in — `domains/<subject>` for a subject,
`interviews/rounds/<round>` for an interview round, `interviews/companies/<co>/deck`
for a company deck (ADR 0008; the slug itself when omitted) — put content under
`vault/<folder>/`, and pass `--domain <domain>` — or `--all` to run any
command across every domain (CI builds all decks). Nothing else changes.
Keep low-level design, domain knowledge, etc. as separate domains; bridge them
with cross-domain wikilinks, which work because `vault/` is one Obsidian vault.

## Development

```bash
pip install -e .[dev]
pytest -q
```

Optional extras: `[clip]` for `trellis clip` (article extraction), `[ingest]`
for pdf corpora (PyMuPDF). Epub, markdown, and web corpora need nothing extra.

CI validates the skeleton, runs the tests, and uploads a fresh `.apkg` on every
push.

## Credits

Topic coverage informed by
[system-design-primer](https://github.com/donnemartin/system-design-primer)
(CC BY 4.0) and *Designing Data-Intensive Applications*. Card text is original.
`.apkg` packaging via [genanki](https://github.com/kerrickstaley/genanki).
