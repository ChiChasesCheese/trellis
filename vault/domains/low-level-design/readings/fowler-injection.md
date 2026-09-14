---
nodes: [principles.coupling]
url: https://martinfowler.com/articles/injection.html
tags: [canonical]
---
# Inversion of Control Containers and the Dependency Injection Pattern (Fowler)

The article that named dependency injection. Explains constructor/setter/
interface injection and service locator as coupling-management strategies —
DI as the tool that turns hard-wired dependencies into swappable seams.

**Extract on read:**
- The core move: a class declares what it needs (constructor parameters) and
  an assembler wires it — the class stops knowing concrete types.
- Constructor vs setter injection trade-offs; prefer constructor for required,
  immutable dependencies.
- DI vs service locator: both decouple, but a locator leaves a hidden
  dependency on the locator itself — worse for tests.

%% trellis:begin %%
## Source
[Open the original ↗](https://martinfowler.com/articles/injection.html)

## Archived copy
![[fowler-injection-clip]]
%% trellis:end %%
