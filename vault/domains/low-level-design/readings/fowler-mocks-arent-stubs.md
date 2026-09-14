---
nodes: [quality.testability]
url: https://martinfowler.com/articles/mocksArentStubs.html
tags: [canonical]
---
# Mocks Aren't Stubs (Martin Fowler)

The canonical article on the test-double taxonomy (dummy, fake, stub, spy,
mock, after Meszaros) and on why designing for substitutable collaborators —
injected through constructors — is what makes code testable at all.

**Extract on read:**
- The five doubles and the split that matters: state verification (stubs/fakes)
  vs behavior verification (mocks).
- A double can only be inserted where a seam exists — dependencies passed in,
  never reached through statics or globals.
- Classicist vs mockist styles and how each drives design (mockist testing
  pushes you toward interface-heavy, injected designs).

%% trellis:begin %%
## Source
[Open the original ↗](https://martinfowler.com/articles/mocksArentStubs.html)

## Archived copy
![[fowler-mocks-arent-stubs-clip]]
%% trellis:end %%
