---
nodes: [runtimes.node-streams]
url: https://nodejs.org/api/stream.html
tags: [canonical]
---
# Node.js Streams API

The authoritative contract for readable/writable streams, `highWaterMark`, `pipeline`, destruction, and abort-aware composition.

**Extract on read:**
- `write() === false` means the producer must wait for `drain`.
- `pipeline()` establishes one error and cleanup boundary across stages.
- Buffer thresholds control flow only when upstream honors them.

%% trellis:begin %%
## Source
[Open the original ↗](https://nodejs.org/api/stream.html)
%% trellis:end %%
