---
nodes:
- platform.pipelines
title: 'The Data Pipeline: Raw, Bars, Panel'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/data-pipeline.md
tags:
- codebase
---

# The Data Pipeline: Raw, Bars, Panel

Describes a three-stage contract for market data: an immutable, append-only raw archive exactly as received from each vendor; a normalized, adjusted, per-instrument bars view derived from it on read; and a point-in-time-masked, survivorship-corrected cross-sectional panel view derived from bars, also on read rather than materialized twice. The key design idea is that raw is the only thing physically stored — correctness fixes and adjustment-convention changes propagate instantly to all downstream consumers without leaving two versions of history to drift apart — and that research code is structurally barred from touching raw files directly, only ever reading bars or panels.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/data-pipeline.md)

## Archived copy
![[qs-data-pipeline-raw-bars-panel-clip]]
%% trellis:end %%
