---
nodes: [quality.smells]
url: https://blog.codinghorror.com/code-smells/
tags: [reference]
---
# Code Smells (Jeff Atwood, Coding Horror)

The whole Fowler/Beck smell catalog compressed into one readable page: every
smell named, described in a sentence or two of plain English, with the
refactoring that cures it. Unlike a catalog index it is actually readable
front to back in ten minutes, which makes it the fastest way to install the
vocabulary you need to answer "what would you improve about this code?".

**Extract on read:**
- The smell families in one pass — duplicated code, long method, large class,
  long parameter list, feature envy, primitive obsession, switch statements,
  shotgun surgery, divergent change, inappropriate intimacy.
- The pairing that matters in an interview: each smell names a *specific*
  refactoring, so "this is feature envy" implies "move method", not vague
  hand-waving about cleanliness.
- The meta-point: a smell is a hint to look, not a proof of guilt — say why
  the smell matters here before you refactor.

%% trellis:begin %%
## Source
[Open the original ↗](https://blog.codinghorror.com/code-smells/)

## Archived copy
![[codinghorror-code-smells-clip]]
%% trellis:end %%
