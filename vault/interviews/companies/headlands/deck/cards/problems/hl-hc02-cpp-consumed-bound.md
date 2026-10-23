---
id: hl-hc02-cpp-consumed-bound
node: problems.hc02-merge-k-streams
type: qa
step: 23
---
## Q
`Pending` 返回时队列里可能已经有数据吗？为什么消费 n 个元素后 source 被取元素的总次数 ≤ k + n − 1？

## A
**`Pending` 时队列里可能已有数据**：`Pending` 的含义是「还有一条活流没有队首」；别的流的队列里可能已经有很多元素，但在那条流给出队首之前不能安全输出。所以它不是「没有数据」。

**≤ k + n − 1**：初始每个 source 取一个队首（k 次）；输出第 j 个元素之后，补位**推迟到下一次调用**，所以输出 n 个元素时最多只补位 n − 1 次（最后一个输出的补位还没发生）。合计 ≤ k + n − 1。两个无限序列（k=2）取前 10 个，只读约 11 个。

**为什么 C++ 的比较器写 `a.stream > b.stream`**：`priority_queue` 弹出比较器意义下「最大」的元素。比较器说「a 排在 b 后面」，最先出来的才是最靠前的：值小的先出，值相等时编号小的先出，所以编号大的才是「后面」那个。

**`const Head& h = heap.top(); heap.pop(); use(h)`**：悬空引用（UB）；应先按值拷出来再 `pop()`。
