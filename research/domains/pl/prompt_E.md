# Card agent — programming-languages domain (`pl`), group E

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never switch branches, never commit, never spawn agents.
You own `vault/domains/pl/cards/<branch>/` for branches **metaprogramming, data, ecosystem, trends, signatures** — nothing else. Scratch work (code you compile
and run) goes in `/tmp/pl_E/`, never in the repo.

## 0. Resume rule

`uv run trellis --domain pl stats` and `ls` your folders; skip leaves that already have cards. `git checkout uv.lock` if
uv touched it.

## 1. Read first

- `skeleton/pl.yaml`: your leaves, their summaries (the summary lists what the leaf must cover) and `requires`.
- `proposals/WRITING_RULES.md` rules 1, 3, 5, 6, 11, 12.
- Format example: `vault/domains/hft/cards/java/hft-java-gc-choices-gen-zgc.md`.

## 2. The goal

Chi (a Java/Python engineer) wants to understand **programming languages from first principles**: what each general
language feature is, why it exists, the design space of solutions, how Go, Java, Rust and Python each answer it, and what
is unique to each — plus how the features map onto the modern evolution of languages. The deck is the main surface:
**cards may be long and should carry examples**. Breadth and structure matter: each leaf is one concept seen through all
four languages (other languages such as C, C++, C#, Kotlin, Swift, TypeScript, Haskell only as contrast when it helps).

## 3. Cards per leaf: 6–8, in this order (`step`)

1. **Principle**: what the concept is and why languages need it; the problem it solves; the design space (the 2–4
   possible approaches) — no language yet, or only as a one-line pointer.
2. **Mechanism**: how it works underneath (memory, compiler, runtime), with a number or a small trace.
3. **Comparison table**: one row per language (Go, Java, Rust, Python), columns chosen for the leaf (approach, syntax
   sketch, guarantee, cost). ≤ 5 rows, short cells, then 2–4 sentences on the pattern the table shows.
4. **Examples**: 1–3 cards with code. One card shows the same task in **at most two** languages side by side (fenced
   blocks, each ≤ 12 lines), so a leaf usually has two example cards covering all four. Say what the output is.
5. **Uniqueness / contrast**: what one language does that the others cannot, or the sharpest contrast pair.
6. **Pitfall / cost**: the classic bug or the price paid, with a code line that shows it.
7. Optional: **history or trend** — where the feature came from and where it is going.

## 4. Card format

```
---
id: pl-<leaf-slug>-<card-slug>
node: <leaf id>
type: qa
step: <n>
---
## Q
<question>

## A
<answer>
```

- `id` lowercase ASCII and hyphens, starts with `pl-`, globally unique; file `<id>.md`. No `source:`, no `tags:`.
- Chinese prose; English terms in full-width parentheses on first use on each card; code identifiers in backticks;
  code comments may be English. No ASCII diagrams; tables ≤ 5 rows.
- **Self-contained**: the question names its subject; the answer defines what it uses, gives the cause → effect, and an
  example or number. Never refer to other cards, sources or books; never 本文 / 本题 / 作者 / 我们认为.
- `trellis validate` warns past 250 whitespace-separated words in an answer (code counts): split a card rather than
  exceed it.

## 5. Correctness (most important)

- **Run every code example** with the local toolchains (Go 1.27, Rust 1.99, Java 25, Python 3.14) in `/tmp/pl_E/`
  and put the real output on the card. A snippet that does not compile must not appear, unless the card is about the
  compile error — then quote the real error message (shortened).
- Version claims ("since Java 21", "Go 1.22 changed loop variables", "Python 3.13 free-threaded build") must be ones you
  are sure of; when a feature is newer than you are sure about, check it with the local toolchain (`go doc`, `javac
  --release 25`, `python3 -c`, `rustc --explain`) or word it without a version.
- Numbers (overheads, sizes, latencies) as magnitudes with 约 / 量级, or measured locally and marked as one measurement.

## 6. Gate (before replying)

1. `uv run trellis --domain pl validate` — 0 errors; no `not_self_contained` / `leans_on_source` / word-count warnings on
   your cards.
2. `uv run python scripts/plain_style.py vault/domains/pl/cards/<branch>/*.md` for each branch — ok.
3. `uv run python scripts/phone_diagrams.py vault/domains/pl/cards/<branch>/*.md` — ok.
4. `uv run trellis --domain pl stats` — every leaf you own has 6–8 cards.
5. `git checkout uv.lock` if changed.

## 7. Reply (≤ 12 lines)

Cards per branch; gate results; how many snippets you compiled and ran; up to 8 claims you are least sure of.
