---
id: leetcode-c-cpython-asyncio-ready-timer-application
node: topics.uncategorised
type: qa
anki: 1787361364023
tags: [algorithm::deque, algorithm::event-loop, algorithm::min-heap, application, case, case::cpython-asyncio-ready-timer, category::runtimes-os, chapter::08, chapter::17, leetcode, system::cpython-asyncio]
---
## Q
CPython asyncio 为什么把 ready callbacks 与 scheduled timers 分别放 deque 和 min-heap？

## A
ready 只需 FIFO append/popleft，deque 常数最小；timer 需要快速找到最早 deadline，min-heap 提供 O(log n) 插入和 O(1) 查看最小值。到期后 timer 再搬进 ready。

**Evidence**

CPython 官方 base_events.py 定义 `_ready` deque、`_scheduled` heap 和 `_run_once` promotion 流程。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FCPython%20asyncio%EF%BC%9AReady%20Deque%20%E4%B8%8E%20Timer%20Heap)
