---
nodes: [runtimes.node-event-loop]
url: https://nodejs.org/learn/asynchronous-work/dont-block-the-event-loop
tags: [canonical]
---
# Do not block the Node.js event loop or worker pool

Node's first-party deep dive into which work runs on the event loop, which APIs use the libuv pool, and how one expensive input becomes a performance and DoS problem.

**Extract on read:**
- Why `async` syntax does not make CPU work nonblocking.
- Which common operations occupy the worker pool.
- How input bounds, partitioning, and offloading protect fairness across clients.

%% trellis:begin %%
## Source
[Open the original ↗](https://nodejs.org/learn/asynchronous-work/dont-block-the-event-loop)
%% trellis:end %%
