---
nodes: [reliability.testing]
url: https://pkg.go.dev/net/http/httptest
---
# Go `net/http/httptest`

Read this to learn the smallest official tools for testing a Handler in memory and across a real HTTP test server. Extract when `ResponseRecorder` is sufficient and when transport behavior requires an actual client/server boundary.

Use those two levels to implement [[reliability-testing-cache-state-matrix]] and [[reliability-testing-real-protocol]]. Header semantics, cancellation, and concurrent origin calls must be asserted as observable protocol behavior, not hidden inside mocks.

%% trellis:begin %%
## Source
[Open the original ↗](https://pkg.go.dev/net/http/httptest)
%% trellis:end %%
