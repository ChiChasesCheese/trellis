---
id: asyncio-pstree-introspection-tool
node: asyncio.debugging
type: qa
source: cpython-internals
---
## Q
想从外部检查一个正在运行的 Python 进程里，各个线程上到底有哪些 asyncio 任务在跑，有什么现成工具？

## A
`python -m asyncio pstree` 可以从外部检查目标进程里所有线程上的任务状态；3.14 起 CPython 把任务列表和当前任务改成按线程各自维护（而不是全局共享一份），正是为了让这类外部诊断工具能可靠地枚举出所有线程上的任务。
