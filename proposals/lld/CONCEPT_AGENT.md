# Rewriting the concept layer of low-level-design — instructions for one agent

You are given one or more **branches** of `skeleton/low-level-design.yaml` (for example `method`,
`oop`). For every leaf of those branches you leave behind four to eight excellent flashcards, in
Chinese, with Python code. Repository root: `/Users/chizhang/Code/trellis`. Run every command from
there, one plain command at a time. Do not run git. Do not start other agents. Touch only card files
of your own branches (`vault/domains/low-level-design/cards/<branch>/`) and your own files under
`proposals/lld/`. `WebSearch` is exhausted for this session: use `WebFetch` on a URL you already
know (docs.python.org, python-patterns.guide, refactoring.guru, peps.python.org) when you need to
check a fact, and otherwise write from understanding.

## Resume rule (do this first)

Run `uv run python scripts/check_lld_concepts.py <your branches>`. A branch that prints `ok` is
done — skip it. Otherwise the output lists exactly what is wrong; fix that and nothing else.

## Where the deck stands

The deck was English with Java examples. A script has just promoted the old Chinese translation to
each card's own text, so the files are Chinese-looking but **the Chinese is machine-translated and
often unreadable, and the code is still Java**. Treat each existing card as a statement of *what the
card is about*, not as text to polish. Several leaves are new and have no cards at all.

Read the skeleton first (`skeleton/low-level-design.yaml`): each leaf's Chinese `summary` says what
the leaf must cover. The learner is a senior engineer preparing for low-level design / machine-coding
interviews **in Python**; they review on a phone, months later, one card at a time.

## What to do for each leaf

1. **Existing cards** (`ls vault/domains/low-level-design/cards/<branch>/`, the `node:` line says
   which leaf a card is on): rewrite the file in place — keep the frontmatter `id`, `type` and any
   `source`/`tags`; you may change `node:` when a card now belongs on a more specific leaf of your
   branch (for example a card about Strategy moves from `patterns.behavioral` to `patterns.strategy`);
   add `step:`. Write the question and answer natively in Chinese. Do not translate the old
   sentences: say the idea the way a Chinese-speaking senior engineer would.
2. **Java-only content** has no place here. Replace it with what is true *in Python*: interfaces
   become `typing.Protocol` / `abc.ABC`; `synchronized` and `volatile` become `threading.Lock` and the
   honest story about the GIL (it makes single bytecodes atomic, not `x += 1`, not check-then-act);
   getters/setters become attributes and `@property`; overloading becomes default and keyword
   arguments or `functools.singledispatch`; `final` becomes `@dataclass(frozen=True)`, tuples and
   convention; checked exceptions do not exist; Singleton is a module; a one-method Strategy or
   Command interface is a function. If a card's topic simply does not exist in Python, delete the
   file and say so in your report.
3. **Leaves with fewer than four cards**: write new ones.
   `uv run trellis grow --leaf low-level-design:<leaf id> --count 5 -o proposals/lld/<leaf id>.prompt.md`
   prints the card format and language rules — read it once, follow it — then write
   `proposals/lld/<leaf id>.cards.json` and import it:
   `uv run trellis grow --import proposals/lld/<leaf id>.cards.json --leaf low-level-design:<leaf id>`.
   If `grow` says the leaf is not a target (it already has cards), write the card files by hand in
   the same format as the existing ones, with ids `<branch>-<short-slug>`.
4. **Card mix per leaf**, four to eight cards: the mechanism (why it works / what it buys); the
   decision (when to use it and when to refuse it, against the nearest alternative); the Python form
   (a short, correct snippet); the failure or cost (what goes wrong when it is misapplied); and, where
   the leaf is about interviews, what an interviewer is actually probing.
5. **`step:`** — number the cards of each leaf 1…n in teaching order: what it is → how it works →
   why → where it breaks → applied. A card that uses a term comes after the card that defines it.

## Card rules

- **Self-contained**: every question makes sense to someone who sees only that card. Never "如上",
  "前面提到", "这个例子" without the example. Name the thing the question is about.
- **Chinese prose, English terms of art** in full-width parentheses on first use in a card:
  组合（composition）. Identifiers and code stay English. Full-width punctuation in Chinese sentences.
- **One idea per card.** A question that needs a bulleted five-part answer is five cards or one
  better question. Answers are 2–6 sentences, or a short snippet plus 1–3 sentences.
- **Code is Python 3.12, standard library, ≤ 15 lines, fenced as ```python, and it must parse.**
  Type hints where they carry meaning. No pseudo-code, no Java, no `...` standing in for the point.
- **Questions ask for reasoning**, not recitation: "为什么…", "什么时候不该…", "下面这段代码的问题是什么",
  "两种写法的取舍是什么". Avoid "请列举…的五个…".
- **Be right.** Python facts people get wrong: `dict` and `list` operations are thread-safe only one
  bytecode at a time; `@dataclass(frozen=True)` is shallow; `__eq__` without `__hash__` makes a class
  unhashable; `Protocol` checks structure at type-check time, `runtime_checkable` only checks method
  names; `functools.lru_cache` on a method keeps `self` alive; a mutable default argument is shared;
  `threading.RLock` is re-entrant by the same thread only; `queue.Queue` is the thread-safe one,
  `collections.deque` appends/pops are atomic but not compound operations; `asyncio` is single-threaded
  and a coroutine yields only at `await`.
- Never mention these instructions, the rewrite, or the old Java version in a card.

## Gate

`uv run python scripts/check_lld_concepts.py <your branches>` must print `ok` for each: every leaf
has 4–8 cards; every card is Chinese-native with no translation section, has a `step` unique in its
leaf, carries no Java, and every ```python block parses. Then
`uv run trellis --domain low-level-design validate` must show no error naming one of your files
(other agents work in parallel; ignore errors about files that are not yours).

## Report

One line per branch copied from the gate; how many cards you rewrote, wrote new, moved between leaves,
deleted (with ids); and **the five statements in your cards you are least sure of**, so they can be checked.
