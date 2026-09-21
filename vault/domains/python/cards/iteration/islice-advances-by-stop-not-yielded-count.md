---
id: islice-advances-by-stop-not-yielded-count
node: iteration.itertools
type: qa
source: python-docs
---
## Q
对一个只能向前走的迭代器（不是 list）用 `islice(it, 2, 5, 2)` 并完整消费它之后，底层的 `it` 被向前推进了几步？和「只产出了 2 个元素」的直觉一致吗？

## A
不一致：不管 `step` 是多少，完整消费 `islice(it, start, stop, step)` 都会把底层迭代器 `it` 向前推进 `max(start, stop)` 步（本例是 5 步），因为它内部要跳过 `[0, start)` 区间并一直读到 `stop` 为止，即使实际产出、被使用的元素因为 `step` 只有 2 个。另外 `islice` 不支持负数的 `start`、`stop`、`step`，这一点和普通序列切片不同。
