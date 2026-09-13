---
nodes: [networking.streaming]
url: https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Concepts
tags: [canonical]
---
# Streams API Concepts (MDN)

The browser API is only one implementation, but this page explains the universal
producer-consumer contract: queued chunks, desired size, readable/writable ends,
and backpressure propagation. Apply the model to every proxy hop.

**Extract on read:**
- Explain how a slow consumer tells a fast producer to pause.
- Separate streaming from unbounded buffering.
- Define what cancellation must release along the entire pipeline.

%% trellis:begin %%
## Source
[Open the original ↗](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Concepts)
%% trellis:end %%
