---
nodes: [concurrency.model, concurrency.primitives, concurrency.hazards, concurrency.patterns]
url: https://jcip.net/
tags: [book, canonical]
---
# Java Concurrency in Practice (Goetz et al.)

Still the definitive treatment of shared-memory concurrency; the mental
model (publication, visibility, safe construction, composing thread-safe
classes) transfers to every language. Chapters 1–5 and 10–11 cover
everything an LLD round can throw at you.

**Extract on read:**
- The Java memory model as "visibility is not atomicity is not ordering."
- @GuardedBy thinking: every mutable field owned by exactly one lock.
- Chapter 10's deadlock taxonomy — lock-ordering vs resource deadlocks.

%% trellis:begin %%
## Source
[Open the original ↗](https://jcip.net/)
%% trellis:end %%
