%% trellis:begin %%
# 上下文管理器：`__enter__`/`__exit__`、`contextlib.contextmanager` 与 `ExitStack`
*迭代器、生成器与上下文管理器*

理解 `with` 如何保证 `__exit__` 在异常时也执行、`__exit__` 返回 True 会吞掉异常、用生成器写上下文管理器时 `try/finally` 包住 `yield`，以及 `ExitStack` 管理动态数量的资源。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/iteration.generators|生成器函数与生成器表达式：惰性、O(1) 内存与一次性]]

## Readings
- [[effective-10-robustness|Effective Python 3e · 第 10 章 健壮性]]
- [[fluent-18-with-match-else|Fluent Python 2e · 第 18 章 with、match 与 else 语句块]]
- [[peps-pep343-with-statement|PEP 343：with 语句的设计取舍]]
- [[py-pydocs-data-model|数据模型（Data Model）参考]]
- [[pydocs-compound-statements|复合语句语法参考：with / try / 泛型参数]]
- [[pydocs-contextlib-module|contextlib 模块：上下文管理器工具箱]]

## Drills
- [[iteration-stream-a-10gb-log|Drill：用生成器管道统计 10 GB 日志的每小时错误数]]

## Cards (6)
1. [[contextmanager-cm-is-single-use]]
2. [[contextmanager-decorator-yield-splits-enter-exit]]
3. [[exit-return-value-suppresses-exception]]
4. [[exitstack-lifo-dynamic-resource-count]]
5. [[swallowing-exception-without-reraise-in-generator-cm]]
6. [[with-statement-desugars-to-try-finally]]
%% trellis:end %%

## Notes
