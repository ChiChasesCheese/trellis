---
nodes: [verification.tests, round.debugging]
url: https://martinfowler.com/bliki/SelfTestingCode.html
tags: [canonical]
---
# SelfTestingCode (Martin Fowler)

Two pages on the property that changes how fast you can work: a suite you can
run in seconds that tells you whether you have broken anything. In a timed round
this is not a quality practice, it is a speed practice — it is what lets you
extend part 3 into part 4 without re-reading part 3. Fowler is also explicit
that a test suite you do not trust is worse than none, because you start
ignoring red.

**Extract on read:**
- Fast feedback as the actual deliverable of testing, not documentation or coverage.
- Why an untrustworthy suite gets ignored, and what makes one trustworthy
  ([[cc-verification-tests-can-it-fail]]).
- Running everything after every change as the habit that catches an extension
  breaking an earlier part ([[cc-verification-tests-two-or-three-per-part]]).

%% trellis:begin %%
## Source
[Open the original ↗](https://martinfowler.com/bliki/SelfTestingCode.html)

## Archived copy
![[fowler-self-testing-code-clip]]
%% trellis:end %%
