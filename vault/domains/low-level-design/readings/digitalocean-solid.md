---
nodes: [principles.solid]
url: https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design
tags: [intro, reference]
---
# SOLID: The First Five Principles of Object-Oriented Design (DigitalOcean)

The most-cited single-page SOLID walkthrough: all five principles with one
compact before/after code example each — ideal for recalling the concrete
violation each principle detects.

**Extract on read:**
- For each principle, the violation smell: SRP = class with two reasons to
  change; OCP = modifying a class to add a case; LSP = subclass breaking a
  caller's expectation; ISP = fat interface forcing no-op methods; DIP =
  high-level code newing up low-level classes.
- The AreaCalculator running example — how one design accretes all five fixes.
- Each fix is a refactoring trigger, not an up-front design mandate.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design)
%% trellis:end %%
