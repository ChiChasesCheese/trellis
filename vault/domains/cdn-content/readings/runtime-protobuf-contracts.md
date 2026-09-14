---
nodes: [runtimes.polyglot]
url: https://protobuf.dev/programming-guides/proto3/
tags: [canonical]
---
# Protocol Buffers proto3 language guide

A concrete, executable model for cross-language schemas. Use it to reason about field identity, unknown fields, defaults, and compatible evolution even when the actual wire format is JSON.

**Extract on read:**
- Why field numbers are durable protocol identity and must not be reused.
- How generated types differ from validation of business invariants.
- Which additive changes preserve old and new readers during version skew.

%% trellis:begin %%
## Source
[Open the original ↗](https://protobuf.dev/programming-guides/proto3/)
%% trellis:end %%
