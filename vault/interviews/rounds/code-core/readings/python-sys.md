---
nodes: [python.io, round.debugging, output.sentinels, input.line-protocols]
url: https://docs.python.org/3/library/sys.html
tags: [docs]
---
# sys — system-specific parameters and functions

The module that owns the three streams your grade depends on. `sys.stdin`,
`sys.stdout` and `sys.stderr` are documented here along with their buffering
behaviour, which explains why debug output and answers interleave oddly in a
terminal and why you must never infer ordering from what you see. Also here:
`setrecursionlimit` for a deep DFS, `intern` for de-duplicating repeated
strings, and `exit` codes.

**Extract on read:**
- `sys.stdin.read()` vs iterating the file object, and `sys.stdin.buffer` for bytes
  ([[cc-python-io-read-all-stdin]]).
- Why every debug line goes to `sys.stderr` and nothing else does
  ([[cc-python-io-stderr-debug]]).
- `sys.setrecursionlimit` and `sys.intern` — two one-line fixes for a stack
  overflow and a memory ceiling.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/sys.html)

## Archived copy
![[python-sys-clip]]
%% trellis:end %%
