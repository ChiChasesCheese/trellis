---
nodes: [oop.interfaces]
url: https://www.artima.com/articles/design-principles-from-design-patterns
tags: [canonical]
---
# Design Principles from Design Patterns — A Conversation with Erich Gamma

The GoF author explaining, in his own words, what "program to an interface,
not an implementation" actually buys — and the one question the Java tutorial
never answers: interface or abstract class?

**Extract on read:**
- The discriminator: an `interface` frees the implementer to pick its own base
  class; an abstract class frees *you* to add methods later with a default.
  Adding a method to a published interface breaks every client.
- Once published, treat an interface as immutable — extend it with a second
  interface (Eclipse's `IWorkbenchPart2` trick), which then pushes an
  instanceof check onto the caller.
- Public ≠ published: a client calling the extra methods on the concrete class
  behind your interface is coding to the implementation and will break.
- Interfaces are the vocabulary of the collaboration — understand the
  interfaces (see `List`/`Set`) and you understand the system.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.artima.com/articles/design-principles-from-design-patterns)

## Archived copy
![[gamma-program-to-interface-clip]]
%% trellis:end %%
