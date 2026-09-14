---
nodes: [networking.protocols, networking.realtime]
url: https://hpbn.co/
tags: [book, canonical]
---
# High Performance Browser Networking (Ilya Grigorik)

The free, canonical book on how TCP, UDP, TLS, HTTP/1.1–HTTP/2, WebSocket,
and SSE actually behave on the wire — written by the engineer who drove much
of this work at Google. Read chapters 1–2 and the XHR/SSE/WebSocket part.

**Extract on read:**
- Latency is dominated by RTTs: handshakes, slow start, and why connection reuse matters.
- TCP vs UDP as guarantee bundles you pay for, not just "reliable vs fast".
- Long-polling vs SSE vs WebSocket: delivery model, proxy friendliness, and connection-state cost.

%% trellis:begin %%
## Source
[Open the original ↗](https://hpbn.co/)
%% trellis:end %%
