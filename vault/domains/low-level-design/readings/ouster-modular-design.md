---
nodes: [structure.api]
url: https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign
tags: [canonical]
---
# Modular Design (John Ousterhout, CS 190 lecture notes)

The free, dense distillation of the interface chapters of *A Philosophy of
Software Design* — deep classes, information hiding, and information leakage,
in the form of the lecture notes Ousterhout teaches from.

**Extract on read:**
- Deep vs shallow: a class earns its interface complexity with hidden
  functionality; if calling the method is barely easier than inlining it, the
  abstraction is a net loss ("classitis" — small classes taken to extremes).
- The interface is everything a caller must know — signatures *plus* the
  informal contract (side effects, ordering, usage constraints), which only
  comments can carry.
- Information leakage is the smell: the same design decision appearing in two
  modules, or a parameter/exception that exists only because the caller knows
  how you store things. Temporal decomposition is its usual cause.

%% trellis:begin %%
## Source
[Open the original ↗](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign)

## Archived copy
![[ouster-modular-design-clip]]
%% trellis:end %%
