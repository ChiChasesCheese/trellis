---
nodes:
- platform.strategy-claim-types
title: 'Alpha, overlay or book: what a result is claiming'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/domain-model.md
tags:
- codebase
---

# Alpha, overlay or book: what a result is claiming

The platform's vocabulary, and one idea in it that generalises: before validating a strategy you must classify what it claims. An alpha claims it predicts direction and answers to a zero-Sharpe null through a deflated Sharpe; an overlay claims it reshapes an existing book's risk, so its null is the un-overlaid benchmark and the question is net gain, not positive return; a book claims a combination beats its parts, so its null is its own best single sleeve. Read the incident that motivates it: six rows that looked like distinct passing alphas turned out to be one risk overlay under six names.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/domain-model.md)

## Archived copy
![[qs-strategy-claim-types-clip]]
%% trellis:end %%
