%% trellis:begin %%
# 健壮性：短 `try` 块、不吞 `Exception`、自定义异常层次与 `warnings`
*工程实践：健壮性、测试与交付*

掌握把 `try` 缩到最小、为库定义根异常隔离调用方、异常变量在块外消失、`assert` 只用于内部假设，以及用 `warnings` 做迁移。

**Requires:** [[domains/python/map/runtime.exceptions|异常：层次结构、`try/except/else/finally`、链式异常与异常组]]

## Readings
- [[effective-10-robustness|Effective Python 3e · 第 10 章 健壮性]]
- [[pydocs-warnings-module|warnings 模块：警告控制]]

## Cards (7)
1. [[robust-assert-internal-invariant-only]]
2. [[robust-except-as-var-cleared]]
3. [[robust-except-exception-specific-first]]
4. [[robust-oserror-hierarchy-catch-root]]
5. [[robust-suppress-vs-bare-except-pass]]
6. [[robust-try-else-minimize-scope]]
7. [[robust-warnings-deprecation-migration]]
%% trellis:end %%

## Notes
