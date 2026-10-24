---
id: tlc-patterns-design-3-why-swap
node: patterns.design
type: qa
step: 3
---
## Q
**数据结构设计题｜正确性：为什么交换删除之后必须更新被移动元素的下标**

RandomizedSet 的删除里，漏掉 `pos[last] = i` 会怎样？设计题里"不变量"指什么？

## A
**不变量（invariant）**：每次操作结束后都应成立的一组条件。RandomizedSet 的不变量是：

1. `len(vals) == len(pos)`；
2. 对每个值 `v`：`vals[pos[v]] == v`。

两条保证 `getRandom` 取到的值存在，`remove` 能通过 `pos` 找到正确位置。

**反例**：依次插入 `1, 2, 3`，删除 `1`，但漏写 `pos[last] = i`。
- 删除后：`vals = [3, 2]`，而 `pos` 里 `3` 的下标仍然是 `2`（应该是 `0`）：`{2: 1, 3: 2}`。
- 再删除 `3`：用 `pos[3] = 2` 去访问 `vals[2]`，越界，抛出 `IndexError`。
- 如果越界没有发生，更糟：会改错位置的元素，数据悄悄损坏。

**检查不变量的做法**：写完每个方法，在方法末尾心里核对一遍上面两条；面试里口头说出："这里我要保证 `vals[pos[v]] == v`，所以移动元素后要更新它的下标。"

- 同一类型的错误：LRU 里只改了链表没改字典；AllOne 里把 key 挪到新桶但忘了更新 `where[key]`。
- 设计题调试方法：每个操作后断言不变量，用随机操作序列和一个朴素参考实现（`set`）对照。
- 复杂度写法：`insert`、`remove`、`getRandom` 平均 `O(1)`（"平均"来自哈希表）。
