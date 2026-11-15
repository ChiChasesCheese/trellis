# Task: bodies for the problems named under 同模式

A card's **同模式** line names up to four related problems, and each unfolds into that problem's own statement and
code. It only unfolds when the problem has a body. 455 named problems have none (Chi, 2026-11-15: 「990 1202 无法展开」).
`research/leetcode-unify/related_missing.json` lists them, most named first: `num`, `slug`, `title` (Chinese), `en`,
`leaf` and `named_by` (the bodies that name it). Your prompt gives you a row range. Repo: `/Users/chiserver/sessions/trellis`.

## Steps

1. **Resume rule.** Skip every row whose `vault/interviews/core/leetcode/problems/<slug>.md` already exists.
2. For each remaining row, write that file. Follow the card rules in `research/leetcode-daily/AGENT.md` § The card
   exactly. Copy the shape of `vault/interviews/core/leetcode/problems/rotting-oranges.md`:
   - frontmatter `slug: <slug>` only;
   - front: `**LC <num> <title>**｜<Easy|Medium|Hard>`, then the **whole** statement in one or two lines (what is
     given, what is asked, a constraint only if the solution depends on it). The statement is shown alone when another
     card unfolds this one, so it must be understandable without the problem page;
   - back: **一句话**, one ```python block (no imports, no type hints, ≤ 60 characters per line), **复杂度**,
     **易错点**, **追问**, **同模式**.
3. **同模式** on the new body: up to 4 problems of the same pattern. Name only problems that already have a body, or
   that are in `related_missing.json`. Look at the body in `named_by[0]` first: its own 同模式 problems are usually the
   right neighbours.
4. **Diagrams.** At least 30% of your bodies get one: a mermaid flowchart, or a bare `<svg>` block (blank line before
   and after, none inside, never fenced). Draw the key move: a window sliding, a union-find merge, a DP table filling,
   a monotonic stack popping. Render-check each mermaid diagram:
   `uv run python -c "import sys; from trellis.build import _mermaid_svg; print(bool(_mermaid_svg(open(sys.argv[1]).read())))" /tmp/x.mmd`
   must print True.
5. **Correctness.** Run every solution on the problem's examples in a scratch file under `/tmp/related_<slug>/`. For
   Hard problems and any problem you are not sure of, also check it against a brute force on ≥ 200 random small
   inputs. Never write the testing process on the card.

## Gate

- `python3 scripts/phone_diagrams.py vault/interviews/core/leetcode/problems` passes.
- `uv run python scripts/lc_tags.py` runs without an error.
- Then run `git checkout -q uv.lock`.
- Do not commit, and do not run `lc_tree.py --write` or anything that touches Anki. Write only the bodies in your row
  range. No subagents.

Reply in at most 5 lines:
- bodies written and bodies skipped;
- diagrams written;
- any solution you could not verify by brute force.
