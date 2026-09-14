---
nodes: [verification.invariants]
url: https://hypothesis.readthedocs.io/en/latest/
tags: [docs]
---
# Hypothesis — property-based testing for Python

The library form of "state an invariant, then let a machine hunt for a
counterexample". You describe the shape of valid inputs, assert a property that
must always hold, and Hypothesis searches — then *shrinks* any failure to the
smallest input that still breaks it, which is the step you would otherwise do by
hand. Even if you never install it in an assessment, reading it teaches the
habit of writing the property first.

**Extract on read:**
- Strategies (`integers`, `lists`, `sampled_from`) as generators of structured
  input ([[cc-verification-invariant-brute-force-oracle]]).
- Shrinking: why a minimal counterexample is worth more than a failing assertion.
- The classic properties — round-trip, invariance, and comparison against a
  simpler model ([[cc-verification-invariant-conservation]]).

%% trellis:begin %%
## Source
[Open the original ↗](https://hypothesis.readthedocs.io/en/latest/)
%% trellis:end %%
