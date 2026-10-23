---
id: hl-heap-debug-deadline
node: foundations.heap-priority-queue
type: qa
step: 38
---
## Q
下面代码想按 `deadline` 从早到晚处理任务，同 deadline 按提交顺序，有什么问题？

```java
PriorityQueue<Task> pq = new PriorityQueue<>(
    (a, b) -> (int) (a.deadline - b.deadline));
pq.add(new Task(3_000_000_000L, "x"));
pq.add(new Task(1, "y"));
System.out.println(pq.poll().name);
```

## A
两个问题：
1. `(int)(a.deadline - b.deadline)`：`long` 差值强转 `int` 会截断。3_000_000_000 − 1 截成 int 是负数，比较器认为 "x" 比 "y" 早，`poll()` 先吐 "x"，而 deadline 更早的是 "y"。用 `Long.compare`。
2. 同 deadline 的顺序没保证（不稳定），需序号字段加 `thenComparingLong(seq)`。

另外 `deadline` 是可变字段，入队后别改。
