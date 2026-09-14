---
nodes: [delivery.flags, delivery.shadow, delivery.canary, delivery.rollback, delivery.cicd]
url: https://sre.google/workbook/canarying-releases/
---
# Google SRE Workbook: Canarying Releases

Read this for the full release experiment: control and canary populations, metric selection, comparison, automation, and rollback. Extract why exposure percentage alone is not evidence and how false positives, false negatives, and cohort selection affect decisions.

Use it as the main source for [[delivery-canary-cohort]], [[delivery-canary-ramp-guardrail]], and [[delivery-canary-significance]]. Feature flags and shadowing are mechanisms that create safer cohorts; the release still needs explicit hypotheses and stop conditions.

%% trellis:begin %%
## Source
[Open the original ↗](https://sre.google/workbook/canarying-releases/)
%% trellis:end %%
