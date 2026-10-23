---
id: hl-hc03-forkjoin
node: problems.hc03-recursive-sum
type: qa
step: 14
---
## Q
用 ForkJoin 并行求和 `long[]`：`RecursiveTask` 怎么写？threshold 怎么选，有哪些坑？

## A
```java
@Override protected Wide compute() {
    if (to - from <= threshold) return sumChunk(data, from, to);
    int mid = (from + to) >>> 1;
    var left = new SumTask(data, from, mid, threshold);
    left.fork();
    var right = new SumTask(data, mid, to, threshold).compute();
    return left.join().merge(right);
}
```
- **只 fork 左半，右半在当前线程算**，再 join 左半；不要两半都 fork（多一次调度）。
- `>>> 1` 而非 `/ 2`：`from + to` 溢出成负数时 `/ 2` 得负，`>>> 1` 仍得正确中点——经典二分 bug。
- **threshold**：太小 → 任务对象 + 调度比加法本身贵（5000 万元素，threshold 100 为 7–8 ms，10⁵ 为 3–4 ms）；太大 → 负载不均。`threshold < 1` 抛 `IllegalArgumentException`；`threshold = 0` 时长度 1 的任务也要拆，`mid == from`，无限递归。块数 > 元素数时要避免 `from > to`。
- `parallelSumStream`：对**块下标**做 parallel stream（`IntStream.range(0, chunks).parallel().mapToObj(...).reduce(Wide.ZERO, Wide::merge)`），不要对装箱的 `Long` 流并行；parallel stream 用公共的 `ForkJoinPool.commonPool()`，会饿死别的任务。
- ForkJoinPool 是专为「大任务拆小任务再合并」的池，空闲线程可「偷」任务。
