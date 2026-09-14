---
nodes: [patterns.structural]
url: https://refactoring.guru/design-patterns/decorator
tags: [canonical]
---
# Decorator (refactoring.guru)

The deep page for the structural family: a full worked derivation (a
notifier that must gain SMS/Slack/email channels) showing why subclassing
explodes combinatorially and how wrapping collapses it. Decorator is also
the pattern most confused with proxy and adapter, and this page's
"Relations with Other Patterns" section is the clearest statement of the
difference anywhere free.

**Extract on read:**
- Composition-over-inheritance made concrete: N features as N wrappers, not
  2^N subclasses — the pricing/discount and stream-wrapping problems both
  reduce to this.
- Decorator vs proxy vs adapter: same shape (an object holding another of the
  same interface), different *intent* — add behavior, control access, convert
  interface.
- The cost: wrapper stacks are hard to debug and order-sensitive, and you
  cannot pull a specific wrapper out of the middle of the stack.

%% trellis:begin %%
## Source
[Open the original ↗](https://refactoring.guru/design-patterns/decorator)

## Archived copy
![[refactoring-guru-decorator-clip]]
%% trellis:end %%
