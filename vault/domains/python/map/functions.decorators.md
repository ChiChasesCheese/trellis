%% trellis:begin %%
# 装饰器：`@` 语法糖、`functools.wraps` 与执行时机
*函数、闭包与装饰器*

理解 `@d` 等价于 `f = d(f)` 且在模块导入时执行、包装函数如何转发参数与返回值、`wraps` 为何要保留元数据，以及叠加多个装饰器的应用顺序。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/functions.scope-closure|作用域（LEGB）、闭包与 `nonlocal`]]

**Unlocks:** [[domains/python/map/functions.decorator-patterns|带参数的装饰器、类装饰器与常见实例（retry、memoize、timing、rate limit）]], [[domains/python/map/functions.functools|`functools`：`lru_cache`、`partial`、`singledispatch`、`cached_property`]]

## Readings
- [[effective-05-functions|Effective Python 3e · 第 5 章 函数]]
- [[fluent-09-decorators-closures|Fluent Python 2e · 第 9 章 装饰器与闭包]]
- [[peps-pep318-decorators|PEP 318：函数与方法的装饰器语法]]
- [[peps-pep612-paramspec|PEP 612：参数规范变量 ParamSpec]]
- [[pydocs-functools-module|functools 模块：高阶函数工具箱]]

## Drills
- [[functions-write-retry-decorator-live|Drill：现场写一个 `@retry(times, exceptions, backoff)` 装饰器]]

## Cards (6)
1. [[decorator-as-function-rewriting-function-pitch]]
2. [[decorator-factory-expansion]]
3. [[decorator-stacking-order]]
4. [[decorator-syntax-equals-reassignment]]
5. [[functools-wraps-preserves-metadata]]
6. [[missing-wraps-failure-mode]]
%% trellis:end %%

## Notes
