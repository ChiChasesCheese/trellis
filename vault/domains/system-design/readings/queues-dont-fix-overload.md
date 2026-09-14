---
nodes: [async.queues]
url: https://ferd.ca/queues-don-t-fix-overload.html
tags: [canonical]
---
# Queues Don't Fix Overload (Fred Hébert)

The antidote to "just put a queue in front of it". Hébert shows with arrival-rate
arithmetic that a queue only buys time: if consumers are slower than producers on
average, the buffer converts a fast failure into an unbounded latency failure.
The best short piece on backpressure and on when async is the wrong call.

**Extract on read:**
- A queue is a buffer, not capacity — it absorbs bursts, never a sustained rate mismatch.
- Unbounded queues turn overload into ever-growing latency plus work nobody is waiting for any more.
- The real levers: bound the queue and choose a shedding policy — drop new, drop old, or push back on the producer.

%% trellis:begin %%
## Source
[Open the original ↗](https://ferd.ca/queues-don-t-fix-overload.html)

## Archived copy
![[queues-dont-fix-overload-clip]]
%% trellis:end %%
