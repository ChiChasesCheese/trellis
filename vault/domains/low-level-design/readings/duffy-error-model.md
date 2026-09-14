---
nodes: [quality.errors]
url: https://joeduffyblog.com/2016/02/07/the-error-model/
tags: [canonical]
---
# The Error Model (Joe Duffy)

The deepest single treatment of error-handling design ever written: a
first-principles comparison of error codes, checked/unchecked exceptions, and
result types, from building a real OS (Midori) that bet on getting it right.

**Extract on read:**
- The foundational split: bugs (programmer errors — assert/fail fast, don't
  handle) vs recoverable errors (expected failures — design as first-class
  return paths).
- Why unchecked exceptions hide control flow, and what typed results/checked
  errors buy at API boundaries.
- Validate at boundaries so interior code can assume invariants instead of
  re-checking everywhere.

%% trellis:begin %%
## Source
[Open the original ↗](https://joeduffyblog.com/2016/02/07/the-error-model/)

## Archived copy
![[duffy-error-model-clip]]
%% trellis:end %%
