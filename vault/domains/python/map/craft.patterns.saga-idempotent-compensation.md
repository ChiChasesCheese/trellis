%% trellis:begin %%
# Saga 与幂等补偿：反向撤销，补偿不能失败也不能重复生效
*编码功力（Coding Craft） / 跨题模式（Patterns）*

跨多个会失败参与方的操作：逐步执行，失败时对失败步和之前所有步按逆序补偿；补偿必须幂等。

**Requires:** [[domains/python/map/runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]], [[domains/python/map/engineering.robustness|健壮性：短 `try` 块、不吞 `Exception`、自定义异常层次与 `warnings`]]

## Cards (5)
1. [[craft-saga-idempotent-compensation-1-reverse-compensation]]
2. [[craft-saga-idempotent-compensation-2-compensate-the-failed-step]]
3. [[craft-saga-idempotent-compensation-3-compensation-errors]]
4. [[craft-saga-idempotent-compensation-4-release-never-raises]]
5. [[craft-saga-idempotent-compensation-5-scales-order-of-steps]]
%% trellis:end %%

## Notes
