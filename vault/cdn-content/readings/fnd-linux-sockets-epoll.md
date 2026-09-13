---
nodes: [foundations.os-io]
url: https://man7.org/linux/man-pages/man7/epoll.7.html
tags: [canonical, reference]
---
# epoll(7) — Linux manual page

The authoritative Linux interface behind many event-driven servers. It is dry,
but it makes readiness, blocking behavior, level- versus edge-triggering, and
the lifecycle of watched file descriptors precise.

**Extract on read:**
- What readiness means—and why it does not promise an operation can never block.
- How edge-triggered code can stall if it does not drain until `EAGAIN`.
- Which FD and event-loop metrics reveal leaks or stalled consumers.

%% trellis:begin %%
## Source
[Open the original ↗](https://man7.org/linux/man-pages/man7/epoll.7.html)
%% trellis:end %%
