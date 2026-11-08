# A framework for coding craft

The `low-level-design` domain began as object-oriented design: classes, patterns, a bank of classic problems. Interviews test more than that. This page says what the
framework covers, why it has this shape, and where its evidence is weak. The skeleton itself is `skeleton/low-level-design.yaml`; the field's outlines are in
`research/domains/low-level-design/FIELD_OUTLINES.md`, and `OUTLINE_MAP.md` beside it checks every topic against a leaf.

## What the evidence says

About 3,400 reports of real craft rounds were collected from public sources, and reduced to about 3,000 after merging the same report seen twice. Each carries a company and a round type, and five in six carry a date. Frequency uses the planner's model (`study-planner.md`): recency, per-company normalisation, shrinkage toward the pooled mix, and a target mix of companies.

| Round type | Share of the index |
|---|---|
| Object-oriented design | 39% |
| Practical / integration | 23% |
| AI-assisted coding | 18% |
| Concurrency | 6% |
| Machine coding | 4% |
| Bug bash | 4% |
| Progressive online assessment | 3% |
| Code review | 2% |
| Extend existing code, API design, language, refactoring, other | 2% in total |

Two facts shape the design.

**OOD is the largest single round, and less than half of the whole.** A deck that teaches only classes and patterns prepares for a minority of what these rounds ask. Practical
rounds alone are more than half the size of OOD, and need skills the OOD material never touches: reading documentation, calling an interface, parsing a messy file, handling a failure.

**Companies differ more than problems do.** In the reports collected, Flipkart's craft rounds are almost all machine coding. Meta's are mostly AI-assisted. Stripe's are practical
rounds and bug bashes. Amazon's are mostly OOD. The same problem is worth different points depending on the round it appears in, so the round is a first-class part of the structure.
Problem frequency is only a second-order guide: the problem bank and the external reports agree moderately on which problems matter (rank correlation 0.46, 9 of the top 20 in common).

## Shape: abilities, then rounds, then problems

The framework has three layers, because they change at different speeds and answer different questions.

1. **Abilities: what you can do.** Grouped from the inside out: the language in your hands (`python`, `fluency`, `languages`); shaping data and interfaces (`oop`, `principles`,
   `patterns`, `data`, `api`, `fsm`); making code correct under stress (`concurrency`, `concurrency-depth`, `errors`, `testing`); moving data in and out (`parsing-io`); working on
   code you did not write (`reading`, `debugging`, `refactoring`, `review`); making it fast (`performance`); and working with tools (`ai`).
2. **Rounds: how an ability is tested.** `method` covers OOD; `rounds` holds one playbook per other round type: its format, what is scored, how to spend the time, and how candidates fail.
   A playbook is short and points at the abilities it draws on.
3. **Problems: where the abilities meet.** `problems` holds classic OOD problems; `amazon` is a company branch; `bank` holds what reports name and the deck lacked, grouped by the
   round each mostly appears in. A problem leaf requires the abilities it exercises.

Each leaf is one thing an interviewer can probe. A topic gets a leaf when at least two independent outlines teach it, or when reports show it being asked.

## How the outlines were used

For each of 15 ability areas, three to seven independent outlines were read: university courses (MIT 6.031, CMU 17-214), official documentation and guides (Python, Go, Google's
engineering practices and API proposals), and the standard books. The skeleton is their union, not a list of what the deck already held. Interview probes for each area test the leaves from the
other direction: a probe no leaf teaches is a gap.

Three areas have weak outlines, and the leaves there rest on more judgement:

- **Reading unfamiliar code:** one real outline (Feathers on legacy code). Few sources teach this systematically.
- **State machines:** practitioner sources only; no university course outline was found at function level.
- **Working with AI tools:** vendor documentation only. It is young and may change fast, and the AI-assisted round itself is changing.

## Decisions worth explaining

**New roots rather than restructuring.** Abilities the old tree partly covered (`concurrency`, `quality`, `structure`) keep their leaves, and the new material is in new roots such as
`concurrency-depth` and `errors`. Existing cards keep their identity and review history, and existing branch orders do not change. The cost is some overlap between old and new; it is resolved
leaf by leaf when low-level design is split from the merged system-design deck and the two are combined.

**Python first; other languages in one branch.** Python is the working language of the deck. `languages` holds only what changes when the language does: error and concurrency models,
modern Java, Go idioms, C++ resource management. `check_lld_concepts.py` still forbids Java everywhere else.

**Empty leaves are the plan.** A leaf with no cards marks what to fill, and the concept gate allows that only in the new roots. A leaf that has cards must meet the same bar as the old ones. Filling goes by value:
abilities most rounds draw on first, then each round's playbook, then problems by frequency.

## Where this is weak

- **Harvest bias.** Search terms were chosen to find craft rounds, so the shares compare craft rounds with each other, not with algorithm rounds.
- **A few sources dominate.** One community bank and one question catalogue supply most rows. The catalogue is company-tagged prompts rather than first-hand reports, so it counts less. Removing the community
  bank replaces 6 of the top 20 problems. The round mix is steadier than the problem ranking.
- **Round types are partly inferred** from titles or catalogue labels, and AI-assisted rounds are recent and concentrated at a few companies.
- **Machine coding is under-reported** in English sources; most of its reports come from forum posts and candidates' repositories, whose company attributions are the authors' own.
- **Thin company samples.** Some target companies have few reports (fewer than 35 for ByteDance and TikTok each), and their mix is pulled toward the pooled one by design.
- **Some sites refuse anonymous reading** (Glassdoor, 1point3acres threads, parts of Blind). They were not forced, so they are under-represented.
- **Coverage is a mapping, not a measurement of quality.** About 39% of problem frequency falls on problems that already have a leaf, and about 21% is a long tail of one-off prompts.
