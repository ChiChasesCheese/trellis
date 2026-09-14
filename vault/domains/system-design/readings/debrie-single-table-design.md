---
nodes: [storage.record-modeling]
url: https://www.alexdebrie.com/posts/dynamodb-single-table/
tags: []
---
# The What, Why, and When of Single-Table Design with DynamoDB (Alex DeBrie)

The standard reference on single-table design: modeling all of an
application's entities in one DynamoDB table with generic PK/SK attributes so
every access pattern is one query, because DynamoDB has no joins and each
request costs a round trip. Equally valuable for its honest list of when *not*
to do it.

**Extract on read:**
- Why no-join stores push you to pre-join data: item collections, generic PK/SK, overloaded indexes.
- Designing from access patterns backward, not from entities forward.
- The downsides: rigid to new access patterns, hostile to analytics, steep learning curve.
- When to skip it (rapidly evolving product, GraphQL-style flexible queries, small scale).

%% trellis:begin %%
## Source
[Open the original ↗](https://www.alexdebrie.com/posts/dynamodb-single-table/)

## Archived copy
![[debrie-single-table-design-clip]]
%% trellis:end %%
