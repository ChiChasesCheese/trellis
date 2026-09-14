---
nodes:
- data.quality
- data.point-in-time.as-of
title: 'Data Governance: Contracts, Catalog, and Health'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/data-governance.md
tags:
- codebase
---

# Data Governance: Contracts, Catalog, and Health

Describes a data-contract discipline: every dataset gets a declarative file stating its schema, coverage window, update cadence, point-in-time correctness, and what counts as valid, which is then automatically checked against reality — freshness SLAs, schema drift, row-count minimums — rather than trusted by convention. The motivating idea is that a strategy's apparent alpha is very often a data artifact — an ex-dividend gap read as a crash, a stale delisted-ticker file — and that a machine-checkable contract catches the mismatch between what a dataset claims to be and what it actually is before it reaches a backtest, rather than after.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/data-governance.md)

## Archived copy
![[qs-data-governance-contracts-clip]]
%% trellis:end %%
