# Card agent — HFT domain, group B

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never switch branches, never commit, never spawn agents, never
touch files outside the folders you own. Shell steps are plain single commands.

**You own**: `vault/domains/hft/cards/<branch>/` for branches **market-structure, protocols, orderbook** — nothing else.

## 0. Resume rule (do this first)

Run `uv run trellis --domain hft stats` and `ls vault/domains/hft/cards/<branch>/` for each branch you own. Skip every leaf
that already has cards. If uv touches `uv.lock`, run `git checkout uv.lock`.

## 1. Read first

- `skeleton/hft.yaml` — your leaves, their titles, summaries and `requires` (what the learner already knows when a card
  comes up; what comes later must not be assumed).
- `proposals/WRITING_RULES.md` rules 1, 3, 5, 6, 11, 12.
- One existing card for format: `vault/domains/kafka/cards/core/kafka-core-batch-latency-throughput-tradeoff.md`.
- Background material already written for this learner (reuse facts and examples, keep numbers consistent):
  - `vault/interviews/companies/headlands/study/30-articles/hc05_market_order_book.md`
  - `vault/interviews/companies/headlands/study/30-articles/hc07_ticker_hash_map.md`
  - `vault/interviews/core/foundations/headlands/networking_basics.md`
  - `vault/interviews/core/foundations/headlands/ordered_maps_trees.md`

## 2. Who reads the cards

Chi: a software engineer (Java / Python), weak fundamentals, preparing for a Java SWE interview at Headlands Technologies
(a proprietary HFT firm) and wanting to understand the whole HFT field well enough to talk about it confidently. Cards are
reviewed cold on a phone in Anki, months later, one at a time, in prerequisite order.

## 3. What a card is

One file per card: `vault/domains/hft/cards/<branch>/<id>.md`.

```
---
id: hft-<leaf-slug>-<card-slug>
node: <leaf id, e.g. java.gc>
type: qa
step: <1..n inside the leaf>
---
## Q
<question>

## A
<answer>
```

- `id`: lowercase ASCII, hyphens only, globally unique, starts with `hft-`; the file name is `<id>.md`.
- No `source:` and no `tags:` line.
- `step`: the order the learner meets the leaf's cards — the basic "what is it / why it works" first, then numbers,
  contrasts, failure scenarios. Steps inside a leaf are 1, 2, 3 … with no repeats.

**Count per leaf**: **5 cards** for leaves under `overview`, `architecture`, `java`, `java-at-hft`, and for leaves marked
`core: true`; **4 cards** for every other leaf. Cover the card mix across a leaf: the mechanism (why it works), the
number or limit (a real magnitude), the contrast with the nearest alternative, the failure or cost scenario (what goes
wrong, what it costs).

**Language**: everything Chinese. Domain terms stay English: on first use on *each card* write the Chinese plus the English
term in full-width parentheses, e.g. 订单簿（order book）, 内核旁路（kernel bypass）; universally English terms (CPU, GC,
JIT, FPGA, TCP, p99) may stay bare. Beginner tone, plain words, like a patient teacher.

**Self-contained and informative — the most important rule.** Chi asked: "not concise, but I should understand fully with
only the card". Every card must be understandable with nothing else on screen:
- The question names its subject (never starts with 它 / 这 / this / it); a short context sentence before the question is
  welcome when the question needs a setting.
- The answer defines every term it relies on that is not in the question (one plain clause each), gives the **cause →
  effect** (why), and anchors with **a concrete number or a small worked example** (e.g. "在 99.99 买 1000 股、100.01 卖出，
  赚 1000 × 0.02 = $20").
- Length: about 150–400 Chinese characters. Use 2–5 short bullet points or a ≤ 4-row table when it helps; bold the key
  words. No ASCII diagrams. Inline code for identifiers (`TCP_NODELAY`, `-XX:+AlwaysPreTouch`).
- Never refer to other cards, readings, talks, books or authors ("如上所述", "某演讲提到", "据 XX 书"); never say where a
  fact comes from. Naming a real system or event as the subject is fine (LMAX, Knight Capital 2012, Aeron, ITCH 5.0).
- Never write 本文 / 本题 / 这道题 / 作者 / 我们认为.
- Numbers: give typical magnitudes with "约 / 量级", not false precision. If you are not sure of a fact, write it more
  generally or leave it out — a confident wrong card is the worst outcome.

The question should be answerable from understanding, not trivia recall: "为什么…", "…和…有什么区别、各自适合什么场景",
"…会出什么问题、代价多大", "…大约是多少、意味着什么". Avoid yes/no questions and multiple choice.

## 4. Gate (run before you reply)

1. `uv run trellis --domain hft validate` — 0 errors, and no `not_self_contained` / `leans_on_source` warnings for your
   cards (the "leaf nodes have no cards yet" warning is fine for leaves you do not own).
2. `uv run python scripts/plain_style.py vault/domains/hft/cards/<branch>/*.md` for each owned branch — no problems.
3. `uv run trellis --domain hft stats` — every leaf you own has the right count.
4. `git checkout uv.lock` if it changed.

## 5. Reply (≤ 15 lines)

Cards written per branch; gate results; then **the claims you are least sure of** (card id + the claim, up to 10) so they
can be checked against a source.
