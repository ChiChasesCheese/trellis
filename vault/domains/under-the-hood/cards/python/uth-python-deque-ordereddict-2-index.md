---
id: uth-python-deque-ordereddict-2-index
node: python.deque-ordereddict
type: qa
step: 2
---
## Q
**deque 的中间下标有多慢**｜Python · CPython 3.14

在 100 万元素的 `deque` 上取 `d[500000]`，比 `list` 慢多少？`deque(maxlen=3)` 又有什么用？

## A
**结构。** 按下标取元素要从离目标近的那一端，沿块链表一块块数过去，每块 64 个。

**细节。**

- 实测：`d[0]`、`d[-1]` 约 0.02 微秒，`d[500000]` 约 20 微秒；`list` 任何下标都是 0.018 微秒。
- 所以中间下标是 O(n)，不要拿 `deque` 当随机访问数组。
- `maxlen=3` 时，满了再 `append` 会从另一端自动丢弃，实测 `0..5` 依次放入后剩 `[3, 4, 5]`。

**为什么。** 链表块换来了两端的 O(1) 和无搬移，中间随机访问就让位了。

**对应 LeetCode：** LC 933 最近的请求次数 · LC 346 数据流中的移动平均数
