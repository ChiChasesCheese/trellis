---
id: uth-python-asyncio-1-loop
node: python.asyncio
type: qa
step: 1
---
## Q
**事件循环一轮做什么**｜Python · CPython 3.14

`asyncio` 的事件循环每轮迭代（`_run_once`）做哪几件事？`await asyncio.sleep(3)` 到时间是怎么被唤醒的？

## A
**结构。** 两个容器：就绪回调的 `deque`（`_ready`），和定时回调的最小堆（`_scheduled`，按触发时间排序），外加一个 `selector` 等 I/O。

**细节。**

- 先算等待时间：`_ready` 非空就是 0，否则取堆顶触发时间减当前时间。
- `selector.select(timeout)` 阻塞等待，I/O 就绪的回调进 `_ready`。
- 堆顶已到期的定时回调逐个 `heappop`，移进 `_ready`。
- 只执行此刻 `_ready` 里的回调，执行中新加的留到下一轮。

**为什么。** 取最近的到期时间只需看堆顶，O(1)，插入 O(log n)；`sleep` 就是用 `call_later` 往堆里放一项。

**对应 LeetCode：** LC 253 会议室 II · LC 295 数据流的中位数
