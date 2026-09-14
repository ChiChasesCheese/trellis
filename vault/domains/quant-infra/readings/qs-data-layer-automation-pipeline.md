---
nodes:
- data.security-master
- platform.pipelines
title: Data Layering and the Alpha Automation Pipeline
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/data-layer-and-automation.md
tags:
- codebase
---

# Data Layering and the Alpha Automation Pipeline

Opens with a real incident — an unadjusted stock spinoff that silently forged a large fake single-day crash in the price history, which two independent cleaning passes both missed — and uses it to motivate keeping a permanent, unedited raw archive plus an independent second vendor for cross-source reconciliation, since two sources built from the same feed can't catch each other's shared bugs. The second half covers designing an unattended, idempotent factor-mining pipeline (archive, stage, mine, sweep, report) that can be safely re-run mid-flight without double-counting trials or corrupting partially-landed data, and that charges every candidate factor against the honest trial count.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/data-layer-and-automation.md)

## Archived copy
![[qs-data-layer-automation-pipeline-clip]]
%% trellis:end %%
