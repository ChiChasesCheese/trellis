---
nodes: [quality.refactoring]
url: https://martinfowler.com/articles/refactoring-video-store-js/
tags: [canonical]
---
# Refactoring a JavaScript Video Store (Martin Fowler)

The famous opening example of *Refactoring*, rewritten by Fowler as a
long-form article with every intermediate step shown and compiled. You watch
one ugly function become a designed object model through named, mechanical
moves — extract function, inline, replace temp with query, move function,
split loop, and finally replace conditional with polymorphism — with the
tests staying green the whole way.

**Extract on read:**
- The rhythm: tiny steps, run the tests after each; a refactoring is
  behavior-preserving *by construction*, not by hope.
- The move that wins LLD interviews: replace conditional with polymorphism —
  the switch on movie type becomes a small type hierarchy.
- Separating calculation from formatting (split phase) is what makes the code
  extensible for a new report type — the classic "now add HTML output" ask.

%% trellis:begin %%
## Source
[Open the original ↗](https://martinfowler.com/articles/refactoring-video-store-js/)

## Archived copy
![[fowler-refactoring-video-store-clip]]
%% trellis:end %%
