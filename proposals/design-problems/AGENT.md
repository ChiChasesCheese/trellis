# Writing one design problem — instructions for one agent

You are given a list of **problem leaves** of the `system-design` domain, e.g.
`problems.social.news-feed`. For each you produce four things, then pass one gate.
Repository root: `/Users/chizhang/Code/trellis`. Run every command from there, one plain
command at a time. Do not run git. Do not start other agents. Touch only the files named
below for your own leaves.

`<slug>` is the last segment of the leaf id (`news-feed`). Your task message gives, per
leaf: the title, the source URLs the survey found, and the concept leaves it stands on.

## Resume rule (do this first, for every leaf)

Run `uv run python scripts/check_design_problems.py <leaf>`. If it prints `ok`, skip the
leaf. Otherwise its output lists exactly what is missing — do only that. Never rewrite a
file that already passes.

## The bar

The reader is a senior engineer preparing for system design interviews who already owns
Alex Xu's *System Design Interview*. **Your solution must be deeper than that book's
chapter on the same problem**: more precise numbers, every major decision argued against
at least two real alternatives, the failure modes and the 10× evolution spelled out, and
the questions a staff-level interviewer asks next. Depth means mechanism and arithmetic,
not length: no filler, no restating the question, no "it depends" without saying on what.

**Every number is computed, never recalled.** Before a figure goes into the article or a card —
QPS, storage, a probability, a ratio, a per-node load — compute it with
`python3 -c "print(...)"` and copy the result. The pilot article stated a birthday-bound
collision probability of 38% where the arithmetic gives certainty (the exponent was off by six
orders of magnitude), and the wrong number had already been copied into a card. Distinguish
"at least one collision ever" from "this insert collides"; average from peak; per-cluster from
per-node. A card inherits its numbers from the article, so fix the article first.

Ground it before you write. Read the free authoritative treatments (the URLs in your
task, `github.com/donnemartin/system-design-primer`, the company's own engineering blog
posts and papers about the real system) with WebFetch/WebSearch. Then **write in your own
words from understanding**. Never copy or closely paraphrase a source's sentences,
structure of bullets, or diagrams. When sources disagree, say so and pick one with a reason.
Do not invent facts about real systems: a number about a real company needs a source link,
otherwise present it as an assumption of this design.

## 1. The solution article

`vault/domains/system-design/readings/problems/solution-<slug>.md`

```
---
nodes: [<leaf id>]
tags: [solution]
---
# 设计题解：<中文题名>（<English name>）
```

No `url:` key — this article is written here. **Chinese prose; technical terms in English,
in full-width parentheses on first use**, e.g. 扇出（fan-out）. At least 9,000 characters.
Exactly these `##` sections, in this order:

1. `## 题目与范围` — the prompt as an interviewer says it; the clarifying questions worth
   asking and the answer each one changes; what is explicitly out of scope.
2. `## 需求` — functional requirements (the 3–5 that drive the design) and non-functional
   ones as numbers: latency targets, availability, consistency, durability.
3. `## 容量估算` — DAU → QPS (average and peak), storage per year, bandwidth, with the
   arithmetic shown, and **which estimate changes which design decision**.
4. `## 核心实体与 API` — entities with their key fields; the API (method, path, params,
   response, idempotency, pagination); what is deliberately not in the API.
5. `## 高层设计` — a ```mermaid diagram (flowchart or sequenceDiagram) and a walk through
   each main request path, component by component, naming the storage technology class
   and why.
6. `## 深入探讨` — at least four `###` deep dives, the hardest parts of this problem. Each:
   the problem stated sharply → at least two real options with what each costs or where
   it breaks → the choice and why → the numbers or data structures that make it work.
7. `## 瓶颈、故障与演进` — hot spots and skew; what happens when each main component
   fails and how the system degrades; what changes at 10× and 100×.
8. `## 面试官会追问什么` — follow-ups grouped by level (mid / senior / staff), each with a
   two-to-four-sentence answer sketch.
9. `## 常见错误` — the mistakes candidates actually make on this problem and the fix.
10. `## 五分钟讲法` — **in English**: the spoken spine of the answer, 8–12 sentences a
    candidate could say aloud to cover the whole design.
11. `## 来源与延伸` — at least three links: what each source adds, and where this article
    disagrees with it. Commercial prep sites are linked, never quoted.

Link the concepts it stands on with wikilinks to their map notes, by node id and title,
e.g. `[[caching.strategies|Write & Read Strategies]]` (your task lists them).

## 2. Source readings (pointers)

One file per source you actually used, at least two:
`vault/domains/system-design/readings/problems/src-<site>-<slug>.md`

```
---
nodes: [<leaf id>]
url: https://…
tags: [no-archive]      # REQUIRED for commercial prep sites; omit for engineering blogs, papers, CC/MIT repos
---
# <The page's own title>
值得读：<两三句中文：它讲了什么、比别处多了什么、哪里和本题解不同>
```

**Mirrors of paid material are not sources.** `Jeevan-kumar-Raj/Grokking-System-Design` and
`liquidslr/system-design-notes` republish a paid course and a paid book. You may read them to
orient yourself, but never add them as readings or link them in the article; cite the original
(the course page or the book, `no-archive`) if you need to credit the idea.

Commercial prep sites (always `no-archive`): hellointerview.com, bytebytego.com,
designgurus.io, educative.io, tryexponent.com, interviewing.io, systemdesignschool.io,
codemia.io, leetcode.com, algomaster.io, systemdesign.one. Note names must be unique in the
whole vault, so keep the `src-<site>-<slug>` pattern. A reading a problem shares with
another leaf may already exist — then add your leaf to its `nodes:` instead of duplicating.

## 3. Cards — six to eight, self-contained

1. `uv run trellis grow --leaf system-design:<leaf id> --count 8 -o proposals/design-problems/<slug>.prompt.md`
2. Read that prompt: it carries the card format and the language rules of this domain
   (English question and answer **plus** a Chinese translation in the same card). Follow it.
3. Write `proposals/design-problems/<slug>.cards.json` — distilled from **your solution
   article**, not from memory. The mix: the numbers that drive the design; the central
   data-model or API decision; two or three of the deep-dive mechanisms; the main trade-off
   against the nearest alternative; a failure or hot-spot scenario; the 10× evolution.
4. `uv run trellis grow --import proposals/design-problems/<slug>.cards.json --leaf system-design:<leaf id>`

**Self-contained** is the rule the importer and the reviewer both enforce: every question
must make sense to someone who sees only that card, months later. Name the system in the
question ("In a news feed design, …"); never say "the article", "as above", "this design",
"the previous card", "our solution". The answer states the mechanism as a fact. Card ids
start with `problems-<slug>-`.

## 4. The drill

`vault/domains/system-design/drills/problems/design-<slug>.md` — unless your task says a
drill already exists for this problem; then add your leaf id to that file's `nodes:` and
extend it rather than creating a second one.

```
---
nodes: [<leaf id>, <the concept leaves it exercises>]
tags: [problem]
---
# Drill: <English prompt as an interviewer would say it>

<Two or three sentences of context and scale.>

**Constraints to state and honor**
- …three or four numbers and hard requirements…

**Grading points**
- <what a strong answer does> ([[problems-<slug>-…]], [[problems-<slug>-…]])
- …at least four bullets, each linking the card(s) that hold the knowledge…

**Solution**: [[solution-<slug>]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
```

Grading-point links must be real card ids (yours, or existing concept cards).

## 5. Card order

Write `proposals/steps/system-design/problems-<slug>.json` as
`{"<leaf id>": ["<card id shown first>", …]}` with every card of the leaf exactly once
(requirements and numbers first, then the central decision, mechanisms, trade-off, failure,
evolution), then `uv run trellis --domain system-design steps --import proposals/steps/system-design/problems-<slug>.json`.

## 6. The gate

`uv run python scripts/check_design_problems.py <leaf id>` must print `ok`, and
`uv run trellis --domain system-design validate` must show no error naming one of your
files (other agents work in parallel; ignore errors about files that are not yours).

## Report

One line per leaf: `<leaf id>: ok` copied from the gate, the article's character count, the
number of cards — and **the three claims in your article you are least sure of**, so they
can be checked.
