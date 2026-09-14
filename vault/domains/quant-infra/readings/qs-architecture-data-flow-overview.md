---
nodes:
- platform.pipelines
- data.point-in-time.universe
title: Architecture and Data Flow (Concept Overview)
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/architecture-and-data-flow.md
tags:
- codebase
---

# Architecture and Data Flow (Concept Overview)

This is the entry-level map of how data and code fit together in a research platform built around three data stages: an immutable raw archive, a normalized single-instrument bars view, and a survivorship-corrected, point-in-time-masked cross-sectional panel view, with bars and panel computed on read rather than stored twice. It also names four narrow extension interfaces (data source, factor, strategy, broker) as the seams where new markets or vendors plug in, and describes a two-stage gate: a cheap research check followed by an execution-realism check, with a strategy only trusted once both pass. Useful as an orientation diagram before reading any single piece of it in depth.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/architecture-and-data-flow.md)

## Archived copy
![[qs-architecture-data-flow-overview-clip]]
%% trellis:end %%
