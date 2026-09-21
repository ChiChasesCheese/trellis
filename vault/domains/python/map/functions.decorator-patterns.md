%% trellis:begin %%
# 带参数的装饰器、类装饰器与常见实例（retry、memoize、timing、rate limit）
*函数、闭包与装饰器*

掌握三层嵌套的参数化装饰器、用类实现带状态的装饰器、装饰方法时 `self` 的传递，以及缓存/重试/限流装饰器的设计要点与可测试性（注入时钟）。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/functions.decorators|装饰器：`@` 语法糖、`functools.wraps` 与执行时机]]

## Readings
- [[fluent-09-decorators-closures|Fluent Python 2e · 第 9 章 装饰器与闭包]]

## Drills
- [[functions-write-retry-decorator-live|Drill：现场写一个 `@retry(times, exceptions, backoff)` 装饰器]]
- [[types-type-a-decorator-and-a-protocol|Drill：给装饰器标注 `ParamSpec`，给鸭子类型参数写 `Protocol`]]

## Cards (6)
1. [[class-decorator-loses-self-binding]]
2. [[decorator-testability-inject-clock]]
3. [[handwritten-memoize-vs-lru-cache]]
4. [[parameterized-decorator-three-layers]]
5. [[rate-limit-decorator-per-function-state]]
6. [[retry-decorator-design-requirements]]
%% trellis:end %%

## Notes
