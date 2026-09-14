---
nodes:
- structure.storage
url: https://martinfowler.com/eaaCatalog/repository.html
tags:
- canonical
- reference
- index
---
# Repository (Fowler, P of EAA catalog)

The canonical definition of the pattern behind every machine-coding storage
layer: a collection-like interface that mediates between domain objects and
whatever holds them — which in an interview is a HashMap you must keep
swappable and thread-safe.

**Extract on read:**
- The contract: domain code sees add/remove/find-by-criteria on an in-memory
  collection illusion; the backing store is an implementation detail.
- One repository per aggregate/entity type, returning domain objects — never
  leaking the underlying map or its iterators.
- The interview extensions the pattern isolates: id generation, secondary
  indexes for queries, and a lock or concurrent map for thread safety.

%% trellis:begin %%
## Source
[Open the original ↗](https://martinfowler.com/eaaCatalog/repository.html)
%% trellis:end %%
