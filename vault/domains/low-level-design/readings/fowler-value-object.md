---
nodes: [oop.values]
url: https://martinfowler.com/bliki/ValueObject.html
tags: [canonical]
---
# ValueObject (Martin Fowler, bliki)

The canonical definition of the entity/value-object split, from the person who
popularized the distinction — short, precise, and linked to the related bliki
entries (AliasingBug, EvansClassification) for the full picture.

**Extract on read:**
- The test: value objects compare by structural equality, entities by identity;
  Money and DateRange vs Customer and Order.
- Make values immutable to kill aliasing bugs — sharing a mutable value is the
  failure mode.
- Whole-value style: replace primitive pairs (amount + currency) with a small
  typed value that owns its own validation.

%% trellis:begin %%
## Source
[Open the original ↗](https://martinfowler.com/bliki/ValueObject.html)

## Archived copy
![[fowler-value-object-clip]]
%% trellis:end %%
