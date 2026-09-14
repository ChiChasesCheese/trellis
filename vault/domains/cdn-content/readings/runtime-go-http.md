---
nodes: [runtimes.go-http]
url: https://pkg.go.dev/net/http
tags: [canonical]
---
# Go `net/http` package

The authoritative reference for the server/client contract used by a Go edge service. Read it to connect handlers and reverse proxies to actual transport lifecycle rather than framework folklore.

**Extract on read:**
- Why `Client` and `Transport` should be reused across goroutines.
- Which timeouts and pool limits exist at client, transport, and server layers.
- Response-body ownership, streaming commitment, and graceful `Server.Shutdown` behavior.

%% trellis:begin %%
## Source
[Open the original ↗](https://pkg.go.dev/net/http)
%% trellis:end %%
