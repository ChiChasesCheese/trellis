---
nodes: [oop.pillars]
url: https://www.infoworld.com/article/2073649/why-extends-is-evil.html
tags: [canonical]
---
# Why extends Is Evil (Allen Holub)

The classic long-form argument that the four pillars are levers with prices,
not virtues: it walks real Java code showing how inheritance shreds
encapsulation, then rebuilds the same reuse with interfaces and delegation.

**Extract on read:**
- The fragile base class problem, demonstrated: a base-class edit silently
  breaks subclasses, and self-use (a base method calling another overridable
  method) makes `CountingSet extends HashSet` double-count.
- Implementation inheritance couples you to base *internals*; interface
  inheritance (`implements`) costs nothing and keeps polymorphism — the
  reason "program to an interface" and composition are the defaults.
- Encapsulation is the pillar that pays for the others: getters that hand out
  internal state, and `protected` fields, are the same leak wearing different
  clothes.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.infoworld.com/article/2073649/why-extends-is-evil.html)

## Archived copy
![[holub-extends-is-evil-clip]]
%% trellis:end %%
