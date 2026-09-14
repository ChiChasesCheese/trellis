---
nodes: [input.normalization, input.grammar]
url: https://docs.python.org/3/library/re.html
tags: [docs]
---
# re — regular expression operations

Read the tokenizer example at the end of the page first: it is a complete,
correct lexer in fifteen lines using one alternation of named groups and
`finditer`, and it is the fastest way to turn a small expression language into
tokens under time pressure. Then read the compilation and flags sections — a
pattern compiled inside a loop is one of the three classic quadratic blowups.

**Extract on read:**
- The "Writing a Tokenizer" example: named groups plus `finditer` as a lexer
  feeding a recursive-descent parser.
- `re.compile` once at module level, never inside the loop
  ([[cc-performance-hot-loop-recompiled-rules]]).
- `re.fullmatch` for validation, non-greedy `*?`, and why `re.split` with a
  capturing group keeps the separators.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/re.html)

## Archived copy
![[python-re-clip]]
%% trellis:end %%
