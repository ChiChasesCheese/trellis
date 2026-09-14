---
nodes: [output.formatting, python.idioms]
url: https://docs.python.org/3/library/string.html
tags: [docs]
---
# string — Format Specification Mini-Language

Byte-exact output is a formatting problem, and this page is the grammar for it:
fill, alignment, sign, width, grouping, precision and type, in that order. The
same mini-language drives f-strings, `format()` and `str.format`, so learning it
once covers every way you will ever render a number. The examples section at the
bottom is the fastest way to see how `{:>10,.2f}` decomposes.

**Extract on read:**
- Width and zero-padding (`{n:05d}`), alignment (`<`, `>`, `^`), grouping
  (`{n:,}`) and fixed decimals (`{x:.2f}`) ([[cc-python-idioms-fstring-format]]).
- `!r` and `!s` conversions — `repr` is what makes stray whitespace visible.
- Rounding in `.2f` is the float's rounding, not your money rule: format at the
  edge, after the arithmetic has already been done in integers.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/string.html)

## Archived copy
![[python-string-format-clip]]
%% trellis:end %%
