---
nodes: [toolbox.union-find, algorithms.graph-traversal]
tags: [stripe-oa, qa12, leetcode]
---
# Drill: evaluate division queries two ways, then find the best rate and the bad quote

Forty-five minutes, stdin to stdout. This is LeetCode 399, Evaluate
Division, the currency-conversion problem in disguise: `A_i / B_i =
values[i]` is a quote, and each query `C_j / D_j` asks for that ratio
through whatever chain of quotes connects them, or `-1.0` if it can't be
derived. Part 1 solves it with BFS over a graph that includes both the
given edge and its inverse. Part 2 solves the same queries with a weighted
union-find, and must agree with Part 1 to within 1e-9. Part 3 assumes the
quotes may disagree with each other and asks for the maximum-product simple
path between two variables, plus the path itself. Part 4 processes the
equations in order and flags any equation whose implied ratio (from the
quotes already accepted) conflicts with its stated value beyond a relative
tolerance — a rejected equation is not applied, so earlier quotes win.

**Constraints to state and honor**
- Up to 20 equations and 20 queries, all values positive; variables are
  short strings, and the given equations are guaranteed consistent for
  Parts 1-2 (contradictions are only introduced in Parts 3-4).
- `x/x` is `1.0` when `x` appears in some equation and `-1.0` when it
  doesn't — a very easy pair to invert by mistake.
- The graph must include the inverse edge (`B -> A` with weight `1/v`) for
  every given equation, in both BFS and union-find.
- Part 3 walks simple paths only — a variable used twice would let a bad
  quote's cycle inflate the product without bound.
- Part 4's tolerance is relative to the stated value, not absolute, and a
  rejected equation must not be folded into the union-find state.

**Grading points**
- Name both techniques and say when each wins: BFS per query is fine for a
  handful of queries, union-find amortizes across many queries after one
  pass of preprocessing.
- The union-find implementation must re-multiply the accumulated weight
  during path compression, not just repoint the parent pointer — this is
  the single most common bug on this problem.
- Part 3's search should keep the best `(product, path)` under an explicit
  tie-break: fewest hops, then lexicographically smallest path — and note
  best is not the same as shortest.
- Part 4 detects a conflict by comparing the union-find's already-implied
  ratio for `A` and `B` against the new equation's stated value before
  deciding whether to union them at all.
- Cross-check Parts 1 and 2 against each other on random consistent input
  as a correctness habit, since they must produce identical answers.
- Edge cases: a disconnected pair of variables; an unknown variable on one
  side of a query; a chain of 20 equations where the product drifts by
  floating-point epsilon but not more; a query in the inverse direction of
  the only known equation.

**Source**
- `vault/stripe/qA12_lc399_evaluate_division/question.md`, `vault/stripe/qA12_lc399_evaluate_division/solution.md`
- `vault/Quick_Check/problems/qA12_lc399_evaluate_division/problem.md`, `vault/Quick_Check/problems/qA12_lc399_evaluate_division/REPORT.md`
- `vault/Quick_Check/study/10-solutions/qA12_lc399_evaluate_division.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):
