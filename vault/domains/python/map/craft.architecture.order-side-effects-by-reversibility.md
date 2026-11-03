%% trellis:begin %%
# 按可逆性给副作用排序：先做会失败的、可回滚的，最后做不可撤销的
*编码功力（Coding Craft） / 架构理解（Architecture）*

多步操作的顺序不是随意的：把最可能失败、最容易撤销的放前面，把无法撤销（出钞、发货、通知）的放最后。

**Requires:** [[domains/python/map/runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]]

## Cards (5)
1. [[craft-order-side-effects-by-reversibility-1-irreversible-last]]
2. [[craft-order-side-effects-by-reversibility-2-extend-before-pay]]
3. [[craft-order-side-effects-by-reversibility-3-failing-step-first]]
4. [[craft-order-side-effects-by-reversibility-4-saga-pairs]]
5. [[craft-order-side-effects-by-reversibility-5-outbox]]
%% trellis:end %%

## Notes
