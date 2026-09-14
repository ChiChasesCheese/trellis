---
nodes: [networking.realtime]
url: https://hpbn.co/websocket/
tags: [canonical]
---
# WebSocket — High Performance Browser Networking, Ch. 17

The chapter itself, not the book's front door: the full WebSocket protocol
walkthrough plus the head-to-head against XHR long-polling and SSE, including
the performance checklist that tells you when *not* to open a socket.

**Extract on read:**
- The HTTP Upgrade handshake, subprotocol negotiation, and why proxies that don't understand it silently break long-lived connections.
- Message framing and the absence of built-in compression/multiplexing — what you have to rebuild yourself on top.
- Connection state as the scaling cost: a WebSocket pins a client to one server process, whereas long-polling and SSE stay request-shaped and load-balance freely.

%% trellis:begin %%
## Source
[Open the original ↗](https://hpbn.co/websocket/)

## Archived copy
![[hpbn-websocket-chapter-clip]]
%% trellis:end %%
