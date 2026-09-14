---
nodes: [distributed.crdt]
url: https://crdt.tech/
tags: [canonical, reference]
---
# CRDT.tech — Conflict-free Replicated Data Types

The community reference site maintained by Kleppmann and the CRDT research
group: one page of intuition, a resource index of the key papers, and links
to production implementations (Automerge, Yjs). The right single entry point
for merge semantics and local-first architecture.

**Extract on read:**
- State-based vs operation-based CRDTs, and the commutative/associative/idempotent merge requirement.
- Why counters, sets (OR-Set), and sequences each need their own construction.
- What CRDTs give up: cross-object invariants still need consensus.

%% trellis:begin %%
## Source
[Open the original ↗](https://crdt.tech/)

## Archived copy
![[crdt-tech-clip]]
%% trellis:end %%
