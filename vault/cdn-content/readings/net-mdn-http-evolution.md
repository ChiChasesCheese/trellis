---
nodes: [networking.http-versions]
url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Evolution_of_HTTP
tags: [canonical]
---
# Evolution of HTTP (MDN)

The clearest compact comparison of why HTTP/1.1 connection reuse, HTTP/2 frames
and multiplexing, and HTTP/3 over QUIC exist. Read it before the individual RFCs
so protocol changes stay tied to the bottleneck each version addresses.

**Extract on read:**
- Identify serialization and head-of-line behavior at each version.
- Explain what HTTP/2 changes without changing HTTP semantics.
- Explain why QUIC moves multiplexing below HTTP and changes loss behavior.

%% trellis:begin %%
## Source
[Open the original ↗](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Evolution_of_HTTP)
%% trellis:end %%
