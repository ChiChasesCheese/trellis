%% trellis:begin %%
# 作用域（LEGB）、闭包与 `nonlocal`
*函数、闭包与装饰器*

掌握名字查找顺序 Local→Enclosing→Global→Builtin、闭包如何持有自由变量的 cell、赋值为何让变量变局部（`UnboundLocalError`），以及循环中闭包的迟绑定陷阱。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.names-objects|名字绑定、对象身份与 `is` vs `==`]]

**Unlocks:** [[domains/python/map/functions.decorators|装饰器：`@` 语法糖、`functools.wraps` 与执行时机]], [[domains/python/map/runtime.namespaces-execution|执行模型：命名空间、`global`、代码块与 `exec`/`eval` 的风险]]

## Readings
- [[effective-05-functions|Effective Python 3e · 第 5 章 函数]]
- [[fluent-09-decorators-closures|Fluent Python 2e · 第 9 章 装饰器与闭包]]
- [[pydocs-execution-model|执行模型：命名空间与作用域]]
- [[pydocs-programming-faq|编程 FAQ：作用域、参数与可变性高频坑]]
- [[pydocs-tutorial-classes|Python 教程第 9 章：类]]

## Drills
- [[functions-write-retry-decorator-live|Drill：现场写一个 `@retry(times, exceptions, backoff)` 装饰器]]

## Cards (6)
1. [[assignment-makes-name-local-statically]]
2. [[global-vs-nonlocal]]
3. [[legb-lookup-order]]
4. [[loop-closure-late-binding-trap]]
5. [[static-scope-dynamic-lookup-pitch]]
6. [[unboundlocalerror-example]]
%% trellis:end %%

## Notes
