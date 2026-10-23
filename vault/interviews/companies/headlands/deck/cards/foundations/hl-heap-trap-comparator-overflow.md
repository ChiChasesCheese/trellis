---
id: hl-heap-trap-comparator-overflow
node: foundations.heap-priority-queue
type: qa
step: 27
---
## Q
`new PriorityQueue<Integer>((x, y) -> x - y)` 有什么 bug？正确写法是什么？`long` 字段 `(int)(a.deadline - b.deadline)` 呢？

## A
减法在差值超过 `int` 范围时溢出，符号错误。放入 `Integer.MIN_VALUE`、1、−1，错误版本的出队顺序是 `-1 1 -2147483648`（`1 - MIN_VALUE` 溢出成负数，比较器误认为 1 小于 MIN_VALUE），正确版本是 `-2147483648 -1 1`。

```java
new PriorityQueue<Integer>(Integer::compare);
```
永远用 `Integer.compare` / `Long.compare` / `Comparator.comparingInt`。

`long` 的差值强转 `int` 同样会截断：3_000_000_000 − 1 = 2_999_999_999 截成 int 是 −1_294_967_297，比较器误认为 deadline 大的更早。用 `Long.compare`。
