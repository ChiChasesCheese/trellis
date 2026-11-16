# LeetCode Project ten-second cards — instructions for the writer and the verifier

Chi learns each LeetCode Project like vocabulary (2026-11-16): he sees a card, knows at a glance whether he knows the
point, taps (never types), and grades himself 1–4. So every card tests **one fine-grained point** and is read and
answered in **ten seconds**; an extension line under the answer adds the next thing a senior engineer would say and does
not count toward the point. A miss sends him back to the knowledge-tree leaves of that point, so the point list and its
leaves matter as much as the cards.

Repository root: `/Users/chiserver/sessions/trellis`. Everything you write is local and private
(`sources/local/lc-project/quick/`): no git, no other agents, no web tools needed.

## Input, for project `<slug>`

- `sources/local/lc-project/workspaces/<slug>/files/`: LeetCode's workspace (README.md = the contract, the template, the
  public tests, REFLECTION.essay).
- `vault/domains/low-level-design/problems/lcp-<slug>/`: our reference `solution.py`, the defective `starter.py` (repair
  projects), our tests, and `points.json` (the project's exam points with knowledge-tree leaf ids).
- `vault/domains/low-level-design/readings/problems/solution-lcp-<slug>.md`: our article (decisions, defects, follow-ups).
- `~/.local/state/lcp-ladder-cards-20261116/<slug>/` if it exists: long cards written earlier, good raw material.
- The leaf ids live in `skeleton/low-level-design.yaml`; `grep -n "id: <leaf>$"` checks one.

## Output

1. `sources/local/lc-project/quick/points/<slug>.json`: the fine-grained points, **in study order** (foundations of the
   contract first, then mechanisms, then pitfalls and agent workflow):
   `[{"kp": "<slug>.<kebab-name>", "title": "<中文短语>", "kind": "<kind>", "leaves": ["<leaf id>", …]}]`.
   Start from `points.json`, split any point that holds two facts, add the README rules it misses. Expect 25–45 points.
   `kind` is one of: `rule` (a contract rule: return shape, boundary, rounding, precedence, what a failure leaves),
   `mechanism` (how the solution makes it true), `pitfall` (a defect or a tempting wrong way), `decision` (a choice with a
   refused alternative), `number`, `agent` (how to direct and verify the coding agent on this project), `test` (what
   test pins a rule). `leaves`: 1–3 real leaf ids, the knowledge a miss sends Chi back to.
2. `sources/local/lc-project/quick/cards/<slug>.jsonl`: one card per point, one JSON object per line, in the same order.
   Every card has `kp`, `fmt`, `more`, `based_on` (a subset of `readme`, `overview`, `template`, `tests`, `solution`,
   `article`, `reflection`, `bank`).

## Formats

| fmt | fields | Chi does |
|---|---|---|
| `mc` | `q`, `opts` (2–3, **the right one first**; the build shuffles), `why` | taps one option |
| `multi` | `q`, `opts` (4–6), `ok` (indices of the right ones: at least one, not all), `why` | taps every right one, then 确定 |
| `bug` | `q`, `code` (4–10 lines, each ≤ 44 characters, real Python), `bad` (index of the one wrong line), `fix` (that line corrected), `why` | taps the wrong line |
| `order` | `q`, `lines` (3–4, in the right order), optional `decoys` (1–2 lines that belong nowhere), `why` | taps 1, 2, 3, 4 on fixed rows (a rank badge per row); skips decoys |
| `judge` | `q`, `rows` (3–5 `[statement ≤ 22, true/false, reason if false]`, mix true and false), `why` | taps ✓ or ✗ on every row |
| `match` | `q`, `pairs` (exactly 3 `[left, right]`), `why` | pairs two columns |
| `cloze` | `text` with exactly one `{{c1::…}}`, `why` | recalls the blank, flips |
| `flaw` | `q` = one statement with exactly one flaw, `a` = what is wrong and the right way | says what is wrong, flips |
| `qa` | `q`, `a` (one phrase) | answers in his head, flips |

Any card may add `snippet` (code on the back); `mc`, `multi`, `qa`, `flaw` may add `code_q` (code with the question).
Every tapped card shows a 不会 button: Chi taps it instead of guessing. An `order` with one adjacent swap tells him to
grade Hard, so a 4-row order card is graded by how far off he was, not all-or-nothing.

**Mix per project: at least 60% tapped** (`mc`, `multi`, `bug`, `order`, `match`), because a tap gives Chi an objective
right or wrong. Use each format where it fits:

- `order` for **sequences that are really sequences**: the steps of a flow ("validate → check key → write → record key"),
  the order rules are applied (error precedence), and Chi's favourite, **the order of thinking**: what a strong
  candidate settles first, second, third when the project opens (read the contract before prompting the agent; decide
  the lock scope before writing code). A wrong order must be a real, tempting mistake.
- `judge` (Kprim) when a point has several near-miss facts: four statements, each judged ✓/✗, each false row with its
  one-line reason. Prefer it to `multi`: every row is judged, so a miss names the exact fact.
- `order` with `decoys` for code-line or step sequences where an extra step is the tempting mistake (`SELECT` before
  `INSERT` for a uniqueness check, a sleep-based retry).
- `multi` when a question has several right answers that a candidate tends to half-know ("which of these leave state
  behind on failure?", "which inputs must be rejected?"). 4–6 options, each a different fact.
- `bug` for a pitfall that lives in a line of code: the boundary `>` vs `>=`, the append before the check, the missing
  commit, the read outside the lock, the shared mutable default. The excerpt is short, runs in the reader's head, and
  has exactly one wrong line; every other line is correct Python.
- `mc` for a decision or a rule with one or two tempting wrong alternatives.
- `cloze` only for a number with its unit or the proper name of a mechanism; `flaw` and `qa` sparingly.

## Content: dense, structured, code first (Chi, 2026-11-16)

Chi: high information per second, the layout shows the outline, no filler, and code instead of prose wherever code says
it ("单纯用文字去讲解，真的会看麻"). So:

- **Ask with code when the point lives in code.** `bug` for a wrong line; `mc`/`multi` whose options are code
  expressions (`tokens >= 1` vs `round(tokens) >= 1`); `cloze` on the one token that matters (`now - ts {{c1::>=}} window`);
  `order` over 3–4 code lines or steps. Put a 1–8 line excerpt beside the question in `code_q` (allowed on `mc`, `multi`,
  `qa`, `flaw`) instead of describing the code in words.
- **Answer with code.** `snippet`: 1–8 lines (each ≤ 44 characters) shown under `why` — the minimal correct code for the
  point. A card about a mechanism almost always has one. `why` then needs only the reason, in one short sentence.
- Both code fields are scanned, not read, so they sit outside the unit limits; keep them real, runnable Python that
  matches our solution's names.
- No filler words ("注意"、"值得一提"、"其实"、"需要"). Every word in `q`, `why`, `more` carries information.

## Ten seconds: the limits (`uv run python scripts/lcp_quick.py gate <slug>` enforces them)

Count a Chinese character as 1 and an ASCII letter or digit as ½; punctuation is free.

- Before the answer: ≤ 55 for `cloze`, `flaw`, `qa`; ≤ 62 for `mc`, `order`, `match`; ≤ 80 for `multi`. A `bug` card's
  question ≤ 55; its code is scanned, not counted, but stays within 4–10 short lines.
- After the answer (answer plus `why`): ≤ 42. Whole card ≤ 90 (≤ 110 for `multi`).
- An option ≤ 16, an order line ≤ 14, a match side ≤ 10, a cloze blank ≤ 14.
- One sentence each; no lists or line breaks; markdown only `` `code` `` and `**bold**`.

## `more`: the extension line

Every card has `more`: one sentence (≤ 45 units), shown under the answer and outside the point's grade. It goes one
step past the card: when the rule stops holding; the cost of the right way; how the hidden test or production would
expose the mistake; the neighbouring idea it is confused with; or how the same point appears in another project or a
classic problem. It never restates the answer and the card stands without it.

## What makes a card good

1. **One point, the core of it.** A reader who knows the point answers at once; one who does not cannot guess.
2. **Self-contained.** Name the system in a few words ("限流器里，…", "幂等创建工单时，…"); never "本题", "上一张".
3. **Right per the README and our solution.** Where the README leaves a choice open and our solution decides it, the
   card says so ("本实现选…") or tests something else. Numbers carry units and conditions; compute them, never recall.
4. **Wrong options are real mistakes** a candidate would make, each clearly wrong in the stated situation, about as long
   as the right one; no "以上都对", no giveaway wording, no two wordings of one mistake.
5. **No giveaway.** Nothing beside a blank or in the stem names the answer; put such hints in `why`.
6. **Chinese, plain and spoken**, terms engineers say in English stay English (`idempotency key`, `TTL`, `lock`).
7. **Vary the openings**; do not start every question the same way.

## Steps (writer)

1. Resume rule: if `points/<slug>.json` and `cards/<slug>.jsonl` exist, write only the points that lack a card.
2. Read every input. Write the points file, then the cards (write files with a Python script or the Write tool; one
   valid JSON object per line, `ensure_ascii` off).
3. Run `uv run python scripts/lcp_quick.py gate <slug>` and fix every failing line (shorten by cutting words, never
   meaning) until it reports 0 failing and 0 without a card. Do not run git; if uv touches uv.lock, leave it.
4. Rewrite the leaf's synthesis cards (`vault/domains/low-level-design/cards/lcproject/lcp-<slug>-*.md`, 3–5 cards) into
   the layout of LCP_AGENT.md §6: keep `id`, `node`, `step`, `tags`; rewrite only the `## A` body (and tighten `## Q`).
   Then run `uv run python scripts/check_lld_problems.py --branch lcproject lcproject.lcp-<slug>`,
   `python3 scripts/plain_style.py <the cards>` and `python3 scripts/phone_diagrams.py <the cards>` until all pass.
5. Report: points per kind, cards per format, the tapped share, cards with code, and the three cards you are least
   sure are correct.

## Steps (verifier)

You did not write the cards. For each card in `cards/<slug>.jsonl`, read its point and the inputs, and judge it cold:
right per the README and the solution; one answer only (try to argue each wrong option is right, try other fillers for a
blank, check the `bug` excerpt has exactly one wrong line and the fix is right); tests the core of its point; readable in
ten seconds; `more` true and adding something. Also check the points file: is any README rule, defect or decision of the
article missing a point? Are the leaves the right knowledge for a miss?

Write one line per card to `sources/local/lc-project/quick/verify/<slug>.jsonl`:
`{"kp": "...", "verdict": "ok"}`, or `{"kp": "...", "verdict": "ok", "more": "<replacement>", "note": "..."}`, or
`{"kp": "...", "verdict": "fix", "card": {the whole corrected card}, "note": "what was wrong"}`, or
`{"kp": "...", "verdict": "drop", "note": "why"}`. Fix inside the card's format first; keep the tapped share ≥ 60%. For
a missing point, add it to the points file and its card to the cards file yourself, and say so. Then run the gate until
it is clean. Report the counts of ok / fix / drop / added and the notes of the fixes.
