---
nodes: [structure.storage]
url: https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design
tags: [reference]
---
# Designing the Infrastructure Persistence Layer (Microsoft .NET Architecture)

The long version of Fowler's one-paragraph Repository stub: where the
repository boundary goes, how many you should have, what it must *not*
expose, and when skipping it is the right call.

**Extract on read:**
- One repository per aggregate root, not per table or per entity — the
  aggregate is the transaction and consistency boundary, so a repository that
  reaches inside it lets callers break invariants.
- The repository interface belongs to the domain, the implementation to
  infrastructure — that inversion is what makes an in-memory fake a drop-in
  and kills the need for a mocking framework in tests.
- Repository vs DAL vs Unit of Work: a repository speaks in domain objects and
  defers the actual commit; a DAL is CRUD-per-table. And repositories are not
  mandatory — for pure read/query paths, going direct is legitimate.

%% trellis:begin %%
## Source
[Open the original ↗](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design)

## Archived copy
![[msdocs-persistence-layer-clip]]
%% trellis:end %%
