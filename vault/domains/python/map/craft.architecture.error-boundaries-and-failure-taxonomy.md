%% trellis:begin %%
# 错误边界与失败分类：哪些吞、哪些抛、哪些变成值
*编码功力（Coding Craft） / 架构理解（Architecture）*

订阅者/回调的异常在边界处隔离；业务拒绝变成带原因的值；可重试与不可重试分类；补偿失败不能被吞。

**Requires:** [[domains/python/map/runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]], [[domains/python/map/engineering.robustness|健壮性：短 `try` 块、不吞 `Exception`、自定义异常层次与 `warnings`]]

## Cards (6)
1. [[craft-error-boundaries-and-failure-taxonomy-1-isolate-at-the-boundary]]
2. [[craft-error-boundaries-and-failure-taxonomy-2-exception-not-baseexception]]
3. [[craft-error-boundaries-and-failure-taxonomy-3-callback-kills-worker]]
4. [[craft-error-boundaries-and-failure-taxonomy-4-name-every-outcome]]
5. [[craft-error-boundaries-and-failure-taxonomy-5-errors-as-values]]
6. [[craft-error-boundaries-and-failure-taxonomy-6-compensation-and-http]]
%% trellis:end %%

## Notes
