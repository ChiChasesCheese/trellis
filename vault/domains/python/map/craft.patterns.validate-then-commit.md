%% trellis:begin %%
# 先校验后提交：失败不留痕迹（validate-then-commit）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

所有可能失败的检查排在任何写入之前；提交段只做「不会再失败」的赋值。

**Requires:** [[domains/python/map/runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]], [[domains/python/map/engineering.robustness|健壮性：短 `try` 块、不吞 `Exception`、自定义异常层次与 `warnings`]]

## Cards (5)
1. [[craft-validate-then-commit-1-write-vs-validate]]
2. [[craft-validate-then-commit-2-across-problems]]
3. [[craft-validate-then-commit-3-composite-limiter-leak]]
4. [[craft-validate-then-commit-4-same-lock]]
5. [[craft-validate-then-commit-5-scales-2pc]]
%% trellis:end %%

## Notes
