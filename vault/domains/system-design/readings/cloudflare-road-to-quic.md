---
nodes: [networking.protocols]
url: https://blog.cloudflare.com/the-road-to-quic/
tags: [canonical]
---
# The Road to QUIC (Cloudflare)

The single best free explanation of *why* the transport stack looks the way it
does: what TCP guarantees cost, where HTTP/1.1 keep-alive and HTTP/2
multiplexing hit their ceiling, and what moving to UDP actually buys. Reads in
20 minutes and leaves you able to argue HTTP/1.1 vs 2 vs 3 on mechanism rather
than version numbers.

**Extract on read:**
- TCP head-of-line blocking: HTTP/2 removed the application-layer queue but the single ordered byte stream underneath re-created it.
- What TCP bundles — ordering, reliability, congestion control, a 1–3 RTT handshake — and which of those QUIC keeps, moves, or drops onto UDP.
- Connection setup as the latency budget: TCP+TLS round trips vs QUIC's 0-RTT/1-RTT, and why connection reuse dominates real page latency.

%% trellis:begin %%
## Source
[Open the original ↗](https://blog.cloudflare.com/the-road-to-quic/)

## Archived copy
![[cloudflare-road-to-quic-clip]]
%% trellis:end %%
