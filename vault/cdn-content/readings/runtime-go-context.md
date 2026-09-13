---
nodes: [runtimes.go-lifecycle]
url: https://go.dev/blog/context
tags: [canonical]
---
# Go Concurrency Patterns: Context

The official explanation of propagating deadline, cancellation, and request-scoped values through a server call tree.

**Extract on read:**
- Derived contexts can shorten but cannot extend a parent deadline.
- All goroutines serving an abandoned request should exit quickly.
- Cancellation is an API-boundary contract, not a local timer attached after the work starts.

%% trellis:begin %%
## Source
[Open the original ↗](https://go.dev/blog/context)
%% trellis:end %%
