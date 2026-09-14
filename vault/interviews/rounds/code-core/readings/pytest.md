---
nodes: [verification]
url: https://docs.pytest.org/en/stable/
tags: [docs]
---
# pytest documentation

The testing tool worth being fluent in before a round rather than during one.
Plain `assert` with rewritten failure messages means a test is one line and its
failure output already shows both sides of the comparison — which is most of
what you need when you cannot attach a debugger. Read the "How-to guides"
section: assertions, parametrizing, fixtures, and running a subset with `-k` so
you can lock one part at a time without re-running everything.

**Extract on read:**
- Assertion introspection: why `assert got == want` beats a hand-written message
  ([[cc-verification-tests-can-it-fail]]).
- `@pytest.mark.parametrize` for a table of edge cases, each reported separately
  ([[cc-verification-tests-table-driven]]).
- `-k` and markers to run one part's tests in isolation, and `-x` to stop at the
  first failure.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.pytest.org/en/stable/)

## Archived copy
![[pytest-clip]]
%% trellis:end %%
