---
nodes: [architecture.discovery]
url: https://microservices.io/patterns/index.html
tags: [reference]
---
# Microservice Architecture Pattern Index (microservices.io)

Chris Richardson's pattern language is the definitive reference for the
plumbing between services — client-side vs server-side discovery, service
registry, self-registration, and the communication-contract patterns around them.

**Extract on read:**
- Client-side vs server-side discovery: who queries the registry, and what each couples.
- Registries need health checking and TTLs — a registry full of dead instances is worse than DNS.
- Contract evolution: consumer-driven contract tests and tolerant readers keep API versioning from breaking consumers.

%% trellis:begin %%
## Source
[Open the original ↗](https://microservices.io/patterns/index.html)

## Archived copy
![[microservices-io-patterns-clip]]
%% trellis:end %%
