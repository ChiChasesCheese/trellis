%% trellis:begin %%
# 常见 bug 与调试：漏 `await`、循环已在运行、异常被吞、`PYTHONASYNCIODEBUG`
*asyncio 异步编程*

能诊断"程序没有输出"的典型原因：协程未被 await、`gather` 未 await、事件循环嵌套（Jupyter）、异常留在未取回的 Task 里，以及 debug 模式与慢回调告警。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/asyncio.gather-wait-timeout|并发组合：`gather`、`wait`、`wait_for`、`timeout` 与 `TaskGroup`]]

## Readings
- [[cpy-asyncio-internals|异步生成器为什么会漏跑 finally，以及 Task 是怎么被追踪的]]
- [[fowler-02-asyncio-basics|Python Concurrency with asyncio · 第 2 章 asyncio 基础：协程、任务、future 与调试]]
- [[pydocs-asyncio-dev-practices|asyncio 开发实践与调试]]

## Drills
- [[asyncio-fix-the-silent-async-script|Drill：一段拉分页 API 的 asyncio 脚本没有任何输出，找出三个 bug]]

## Cards (6)
1. [[async-generator-not-fully-iterated-finally-may-not-run]]
2. [[asyncio-pstree-introspection-tool]]
3. [[debug-mode-catches-wrong-thread-calls]]
4. [[debug-mode-four-ways-to-enable]]
5. [[debug-mode-slow-callback-100ms]]
6. [[task-exception-never-retrieved-log]]
%% trellis:end %%

## Notes
