# The vault decides the order and the mix Anki deals

Trellis has always claimed to introduce cards "in the order the skeleton
prescribes". Checked against the live collection on 2026-09-19, it did not.
Three things stood between the claim and the phone:

- **Position was an accident.** Anki deals new cards by a number each one
  carries, its position. `build` never set it, so a card took whatever place
  it had in the package the first time it was imported — and kept it for
  good, because Anki's importer places notes it has never seen and leaves the
  rest where they are. Reordering, inserting or re-prioritising anything in
  the vault changed nothing a learner would ever see.
- **Decks are dealt alphabetically.** The default preset gathers new cards
  deck by deck, and only top-level decks carry an ordinal. Inside a branch
  the leaves were studied in the order of their titles.
- **Inside a leaf, file names decided.** `cache-model-hit-ratio` came before
  `cache-model-what-is` because h sorts before w.

And nothing at all said how much of a day should be new material, or what
should come first when there is not time for everything.

## Sequence

A domain has one **Sequence**: every card Trellis owns, in the order it
should first be met. It is a pure function of the skeleton and the cards
(`trellis/sequence.py`), made of two decisions.

**Which leaf first: the Core, then the rest.** Each pass runs in the
skeleton's tree order, which validation already guarantees never puts a leaf
before what it requires; and the Core is closed under `requires`, so neither
pass can either. This is the 80/20 made operational — one short pass through
what matters most, in textbook order, before the long one — rather than a
priority sort that would hop between branches card by card.

The Core is **declared**: `core: true` on a leaf, or on a branch to cover its
subtree, plus everything those leaves require. Bearing was the first
candidate and is only the fallback, for a skeleton that declares nothing. It
counts what stands on a leaf, and with `requires` graphs as thin as ours (22
edges in system-design, 12 in kafka — ADR 0005's standing risk) that is not
centrality: computed from bearing alone, system-design's Core contained LLM
foundations, because three AI leaves need it, and did not contain
replication, partitioning or caching. Only an author knows what the heart of
a subject is; the graph's job is to make sure the heart arrives with its
ground under it.

**Which card first inside a leaf: its `step`.** A card file may say `step: 2`.
Stepped cards come first in step order, then unstepped ones, then grown cards
— a second route is only useful once the first has been tried — with the file
name breaking ties so the order is the same on every machine. Two cards of a
leaf claiming one step is a validation error.

Steps are a teaching judgement, so they are asked for, not computed:
`trellis steps -o prompt.md` writes the question, a Runner answers with
`{leaf: [card ids in order]}`, and `--import` accepts it only if every leaf
comes back as exactly its own cards, each once. It then writes one line into
each card file and touches nothing else.

## How it reaches Anki

1. `build` numbers the notes 1…n in Sequence — that is what a fresh
   collection studies in — and tags every Core card `trellis::core`, so the
   Core is something Anki can be *asked* for (a search, a filtered deck), not
   only an order it is shown in.
2. `anki-push` (and `anki-align`, which imports nothing) then **converges**
   the collection: every card of the domain that Anki still calls new is
   given its Sequence position. A card that has been answered is never
   touched — its `due` is a date the scheduler chose. A push that changes
   nothing moves nothing.
3. The domain's decks are put on **a preset of their own**, `Trellis · <title>`,
   cloned from whatever they were using so that everything Trellis has no
   opinion on (FSRS parameters, learning steps, timers) comes along — and set
   to gather new cards by lowest position and show them as gathered. Without
   this step the positions exist and are ignored. The preset it was cloned
   from, which the rest of the collection shares, is never written to.

## Pace

A skeleton may say how its day is split:

```yaml
study:
  order: core-first        # or `skeleton`, the plain tree order
  mix: new-first           # new-first | mixed | reviews-first
  new_per_day: 20
  reviews_per_day: 100
```

`mix` is Anki's own new/review order. There is no ratio knob in Anki and
Trellis does not invent one: **half and half is equal limits, mixed**
(`mix: mixed`, `new_per_day: 20`, `reviews_per_day: 20`). Every key is
optional; a key that is absent is never written, so a domain that sets no
Pace changes only how its new cards are gathered.

One thing Trellis cannot set: in the v3 scheduler the review limit caps new
cards too — reviews are gathered first and every one of them shrinks the room
left for new cards — unless *Deck options → New cards ignore review limit* is
on. That switch is collection-wide and AnkiConnect cannot reach it. With a
small backlog it does not matter; with a backlog at or above
`reviews_per_day`, `new-first` would show no new cards at all. It is one
checkbox, and it is the only manual step in this design.

## Considered and not done

- **Sorting leaves by bearing, or a weight per node.** A priority sort
  interleaves branches and loses the run of a topic; a numeric weight invites
  tuning that a two-pass order does not need.
- **Card order by convention** (file-name prefixes, or "qa before cloze").
  It would have needed 800 renames, and a card's id is its identity in Anki.
- **One preset for all Trellis domains.** A Pace is per domain by nature — a
  subject being crammed and one being maintained want different days.
- **Writing positions for reviewed cards, or `forgetCards` to restart them.**
  That is rewriting the learner's history to suit the map.

## Risks worth recording

- The domain preset is a *copy*. FSRS parameters optimised later on the
  preset it came from will not follow; optimise the `Trellis · …` preset too.
- `setSpecificValueOfCard` writes a column directly. It is guarded three ways:
  only `due`, only on cards whose `type` is new as read in the same run, and
  the e2e suite fails if a reviewed card's `due` ever changes.
- The Core is an opinion. On system-design 20 declared leaves become 25 of 76
  once their prerequisites are pulled in (160 of 465 cards); on kafka 10
  declared nodes are 14 of 66 leaves (76 of 340 cards). If the first pass
  feels long, the fix is to undeclare, not to weaken the closure.
