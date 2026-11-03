%% trellis:begin %%
# 异常家族：基类 + 多重继承 + 携带数据（typed errors）
*编码功力（Coding Craft） / 高级写法（Idioms）*

每个模块一个基类；再混入 ValueError/LookupError/KeyError 保持标准库兼容；异常带字段，不让调用方去解析消息。

**Requires:** [[domains/python/map/runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]], [[domains/python/map/engineering.robustness|健壮性：短 `try` 块、不吞 `Exception`、自定义异常层次与 `warnings`]]

## Cards (6)
1. [[craft-exception-family-1-base-plus-stdlib-mixin]]
2. [[craft-exception-family-2-carry-data]]
3. [[craft-exception-family-3-value-or-exception]]
4. [[craft-exception-family-4-cause-and-keyerror]]
5. [[craft-exception-family-5-exception-vs-baseexception]]
6. [[craft-exception-family-6-scales-retryable]]
%% trellis:end %%

## Notes
