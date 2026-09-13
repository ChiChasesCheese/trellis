---
nodes: [runtimes.go-concurrency]
url: https://go.dev/blog/pipelines
tags: [canonical]
---
# Go Concurrency Patterns: Pipelines and cancellation

The Go team's complete worked example of fan-out, fan-in, channel ownership, cancellation, and goroutine leak prevention.

**Extract on read:**
- The rule that the sender owning completion closes a channel.
- Why downstream early exit can strand upstream goroutines.
- How cancellation turns a pipeline into a bounded lifecycle rather than background leakage.

%% trellis:begin %%
## Source
[Open the original ↗](https://go.dev/blog/pipelines)
%% trellis:end %%
