# Edit agent — add C++ to the existing comparison cards of the `pl` deck, group T1

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never switch branches, never spawn agents. Scratch in
`/tmp/pl_T1/`. You may **edit** cards in `vault/domains/pl/cards/<branch>/` for branches **foundations, binding, types, abstraction, memory, errors** only; never
create or delete files there, never change `id`, `node` or `step`.

Chi (2026-10-24) widened the deck from four languages to five: C++ joins Go, Java, Rust and Python. A new `cpp` branch
(written by another agent) teaches C++'s own mechanisms; your job is to make the existing cards of your branches compare
five languages where C++ adds something:

1. For every leaf, find its trade-off comparison card (the table with one row per language). Add a **C++ row** with the
   same columns (C++'s choice, what it buys, what it costs), and extend the paragraph under the table by one or two
   sentences on where C++ sits and why (zero-overhead principle, C compatibility, manual control). Tables may now have 6
   rows. If the question says 四门语言 / Go、Java、Rust、Python, update it to include C++.
2. Where another card of the leaf (principle, philosophy, best practice, pitfall, evolution) states something that is
   false or incomplete once C++ is included (e.g. "only Rust has RAII", "no mainstream language does X"), fix it.
3. Do not add C++ to leaves where it has nothing distinct to say (e.g. Python's GIL, CPython internals, gradual typing);
   list those leaves in your reply.
4. A C++ term a card now uses must be glossed in that card in one clause (the `cpp` branch comes later in study order).
5. Any C++ code you add: ≤ 12 lines, compiled and run with `clang++ -std=c++23 -Wall -Wextra` (sanitizers when relevant),
   real output quoted. Keep the senior framing: reasoning, trade-offs and best practice, not syntax.
6. Keep each answer ≤ 250 whitespace-separated words (`validate` warns past it): split nothing — tighten wording instead.

Gate: `uv run trellis --domain pl validate` 0 errors and no `not_self_contained` / word-count warnings on your cards;
`uv run python scripts/plain_style.py` and `scripts/phone_diagrams.py` ok on every file you edited; `git checkout uv.lock`.
Reply ≤ 10 lines: leaves updated, leaves skipped (why), C++ snippets run, claims you are least sure of.
