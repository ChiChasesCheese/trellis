---
nodes: [networking.dns]
url: https://www.cloudflare.com/learning/dns/what-is-dns/
tags: [intro, reference]
---
# What is DNS? (Cloudflare Learning Center)

The most approachable authoritative walkthrough of the resolution path —
recursive resolver, root, TLD, authoritative — with sibling pages on record
types, TTL, and DNS-based load balancing, from a company that runs 1.1.1.1.

**Extract on read:**
- The four servers in a lookup and where caching short-circuits each hop.
- Record types that matter in design: A/AAAA, CNAME, NS, and why apex domains constrain you.
- TTL as a blunt instrument: low TTL for failover agility vs cache-hit efficiency.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.cloudflare.com/learning/dns/what-is-dns/)

## Archived copy
![[cloudflare-dns-clip]]
%% trellis:end %%
