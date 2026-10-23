---
id: hl-hc09-topevents-code
node: problems.hc09-top-trades-by-notional
type: qa
step: 4
---
## Q
写出 `topEvents` 的核心代码：堆、快速拒绝、输出顺序，以及为什么快速拒绝必须严格小于。

## A
```java
var heap = new PriorityQueue<Trade>(Math.max(1, Math.min(k, n)), BEST_FIRST.reversed());
for (int i = 0; i < n; i++) {
    long notional = notionalAt(tickers, prices, volumes, i);      // 校验 + multiplyExact
    if (k == 0) continue;
    if (heap.size() == k && notional < heap.peek().notional()) continue;   // 快速拒绝
    var t = new Trade(i, tickers[i], prices[i], volumes[i]);
    if (heap.size() < k) heap.add(t);
    else if (BEST_FIRST.compare(t, heap.peek()) < 0) { heap.poll(); heap.add(t); }
}
var worstFirst = new ArrayList<Trade>(heap.size());
while (!heap.isEmpty()) worstFirst.add(heap.poll());
return List.copyOf(worstFirst.reversed());
```
- **快速拒绝**：堆满后先拿 `long` 和堆顶 notional 比，严格小就 `continue`，连 `Trade` 对象都不建。随机输入**零分配**，主循环是两次数组读取 + 一次乘法 + 一次比较。正确因为 `BEST_FIRST` 第一条就是 notional 降序。最坏：notional 严格递增时每个元素都进堆，真正 O(n log k)：n=10⁶、k=1000 约 120 ms（随机顺序只要几毫秒）。
- **必须严格 `<`**：写成 `<=` 会把「notional 相同但 ticker 更小」的更好事件也拒掉（下标 1 对下标 4 的样例会错）。
- `BEST_FIRST.compare(t, heap.peek()) < 0` 表示 t 排堆顶前面即更好。
- 不用「`add` 后 `size() > k` 就 `poll`」：也对更短，但每个元素两次堆操作。
- `poll` 出来是从差到好；`ArrayList.reversed()`（Java 21 视图）得从好到差，`List.copyOf` 变独立不可变副本；备选 `new ArrayList<>(heap)` 再 `sort(BEST_FIRST)` O(k log k)。
- 初始容量 `max(1, min(k, n))`：不能为 0，没必要大于 n。C++ 里 `reserve(k)` 在 k=INT_MAX 时有问题，用 `min(k, n)`。

基线 `topEventsSorted`：建 n 个对象整体排序 O(n log n)、O(n) 空间；n=10⁶、k=100、5000 个 ticker 随机顺序：排序约 220 ms，堆约 2–14 ms（含 JIT 预热）。
