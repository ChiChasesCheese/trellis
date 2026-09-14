# Translating cards

This spec is for a domain written in English that carries a Chinese
translation. A domain written in Chinese from the start (`lang: zh` in its
skeleton — a subject digested from a Chinese book) has no English original
and needs none of this; only the rule on technical terms applies to it.

A card written in English keeps that English forever. A translation is
**added beside it**, never in place of it, so a bad translation is always one
deletion away from being undone and the deck still builds if a card was missed.

## Where the translation goes

**qa card** — append two sections after `## A`:

```markdown
## Q
A hot key expires and 10k requests hit the database at once. Name the failure
and two mitigations.

## A
**Cache stampede.** Request coalescing (one recomputes, rest wait) or
jittered/early refresh so keys never expire under full load.

## Q zh
一个热点 key 过期，1 万个请求同时打到数据库。这个故障叫什么，两种缓解手段是什么？

## A zh
**缓存击穿（cache stampede）。** 请求合并（只让一个请求回源重算，其余等待或读旧值），
或者给 TTL 加抖动、提前刷新，让 key 不会在满负载下同时过期。
```

**cloze card** — append one section at the end:

```markdown
Leaderless replication needs {{c1::W + R > N}} to guarantee read-your-writes.

## zh
无主复制要保证 read-your-writes，需要 {{c1::W + R > N}}。
```

## Rules

1. **Never touch the frontmatter or the English sections.** Append only.
2. **A cloze translation must test exactly what the English one tests.** Prose
   inside a deletion *should* be translated — an answer you are meant to produce
   belongs in the language you are studying in. Two things may not change, and
   `trellis validate` rejects the card if they do:
   - **The set of deletions.** If the English card has `c1 c2 c3`, so does the
     Chinese one. Dropping `c3` silently deletes a probe; adding `c4` invents
     one. This is the single most common failure — check it before saving.
   - **The numbers inside a deletion.** `~0.5 ms` stays `~0.5 ms`; `W + R > N`
     stays `W + R > N`. A re-worded quantity teaches something false.
3. **Technical terms stay in English.** Write natural Chinese around them:
   quorum、write skew、idempotency key、LSM-tree、outbox、backpressure、
   implementation shortfall. On a term's first appearance in a card you may
   gloss it once — 缓存击穿（cache stampede）— but do not invent Chinese
   equivalents for terms the field uses in English.
4. **Code, identifiers, formulas, numbers, and product names are untouched**:
   `SELECT ... FOR UPDATE SKIP LOCKED`, `W + R > N`, `p99`, Kafka, Postgres,
   DynamoDB, `principles.coupling`.
5. **Keep the markdown structure** — the same bullets, the same bold, the same
   code fences, in the same order. If the English answer is three bullets, the
   Chinese answer is the same three bullets.
6. **Translate the meaning, not the words.** These are interview flashcards read
   under time pressure: write the Chinese a senior engineer would actually say.
   Awkward literal translation is worse than English.
7. **Skip nothing.** Every card in your batch gets its translation.

## Verify

```bash
cd ~/Code/trellis && uv run trellis --all validate
```

Zero errors. The parser rejects a translation that is missing half a qa pair or
that dropped a cloze deletion, so a clean validate means the structure survived.


## Why this spec is strict (an audit, and what it found)

The first pass used the cheapest available model on all 516 cards. It handled
prose well and failed in a way no amount of instruction prevents: on roughly
40% of sampled cards it did not translate at all. It read the card's topic and
**wrote a new card from its own knowledge** — a plausible question with a
plausible answer that contradicted the original.

Sampling 40 cards by hand put the rate at 16 wrong, 1 drifting, 23 clean, and
the damage was not spread evenly: `low-level-design/oop/` was 7 of 7 corrupt
and `system-design/distributed/` 7 of 8, while everything else sat near 8%.

Two signatures came out of that audit, and both are now mechanical:

- **A rewritten question.** Every corrupted card had a `## Q zh` that was not a
  translation of its `## Q`. If the Chinese question is not the English
  question, the answer below it is invented. This is the check a human (or a
  strong model) should run first when repairing.
- **An invented code block.** A `## A zh` carrying a fenced block the English
  answer never had marked corrupted cards and nothing else. `trellis validate`
  reports these, and `trellis build --lang zh` refuses to ship until they are
  repaired.

The practical rule: a cheap model can restructure text, but high-fidelity
translation of dense technical prose needs a stronger one. Translate with at
least a mid-tier model, then audit a random sample by hand before trusting the
batch — the structural checks catch broken cards, not confident wrong ones.
