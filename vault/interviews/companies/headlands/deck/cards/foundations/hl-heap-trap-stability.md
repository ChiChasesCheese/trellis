---
id: hl-heap-trap-stability
node: foundations.heap-priority-queue
type: qa
step: 25
---
## Q
`PriorityQueue` 对相同优先级的元素保证按插入顺序出队吗？订单簿的「价格-时间优先」怎么实现？

## A
**不保证**（Javadoc：ties are broken arbitrarily）。实测 8 个任务优先级交替 0, 1, 0, 1…、到达顺序 t0…t7，优先级 0 的四个任务出队顺序是 t0 t4 t6 t2，不是到达顺序 t0 t2 t4 t6。这是堆内部结构造成的，依赖实现细节，换个 JDK 版本都可能变。

修法：给每个元素一个单调递增序号，比较器加 `thenComparingLong(seq)`：
```java
record Entry(String name, int priority, long seq) {}
new PriorityQueue<>(Comparator.comparingInt(Entry::priority)
                              .thenComparingLong(Entry::seq));
```
加序号后输出变成 t0 t2 t4 t6 t1 t3 t5 t7。订单簿同价位先到先得必须这样做。
