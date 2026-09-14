---
nodes: [networking.api-styles]
url: https://aws.amazon.com/compare/the-difference-between-grpc-and-rest/
tags: [intro, reference, amazon]
---
# The Difference Between gRPC and REST (AWS "Compare" series)

A vendor-neutral-in-practice, stable comparison of the two dominant service
API styles — coupling, streaming, browser support, payload format — with a
sibling page (the-difference-between-graphql-and-rest) completing the trio.

**Extract on read:**
- gRPC: contract-first Protobuf + HTTP/2 streaming — best inside the datacenter, weak in browsers.
- REST: loose coupling and cacheability — the default when you don't own every client.
- GraphQL (sibling page): client-shaped queries traded against server complexity and cache misses.

%% trellis:begin %%
## Source
[Open the original ↗](https://aws.amazon.com/compare/the-difference-between-grpc-and-rest/)

## Archived copy
![[aws-grpc-vs-rest-clip]]
%% trellis:end %%
