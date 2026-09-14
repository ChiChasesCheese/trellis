---
nodes: [ai.evals]
url: https://hamel.dev/blog/posts/evals/
tags: [canonical]
---
# Your AI Product Needs Evals (Hamel Husain)

The essay practitioners actually pass around on evaluating LLM systems:
a concrete three-level architecture — assertions, human + model grading,
production A/B — built from a real product, with the workflow (look at your
data, log traces, curate failure cases into regression tests) spelled out.

**Extract on read:**
- Level 1 unit-test assertions run on every change; Level 2 human/LLM-as-judge on samples; Level 3 online A/B.
- LLM-as-judge must itself be validated against human labels before you trust it.
- The flywheel: production traces -> reviewed failures -> new eval cases -> prompt/pipeline fixes, forever.

%% trellis:begin %%
## Source
[Open the original ↗](https://hamel.dev/blog/posts/evals/)

## Archived copy
![[hamel-evals-clip]]
%% trellis:end %%
