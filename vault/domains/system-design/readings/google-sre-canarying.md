---
nodes: [infra.delivery]
url: https://sre.google/workbook/canarying-releases/
tags: [canonical]
---
# Canarying Releases (Google SRE Workbook, ch. 16)

The rigorous treatment of progressive delivery: canaries as a statistics
problem (enough traffic to detect regressions, small enough to bound blast
radius), not just "deploy to 5% first". Generalizes to blue-green, feature
flags, and config changes — which the chapter insists are deploys too.

**Extract on read:**
- Sizing the canary population against the error rates you need to detect.
- Choosing canary metrics: leading indicators tied to SLIs, evaluated automatically.
- Roll-forward vs rollback mechanics, and why config/flag changes need the same pipeline.

%% trellis:begin %%
## Source
[Open the original ↗](https://sre.google/workbook/canarying-releases/)

## Archived copy
![[google-sre-canarying-clip]]
%% trellis:end %%
