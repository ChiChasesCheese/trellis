---
id: chain-concatenates-lazily-yield-from
node: iteration.itertools
type: qa
source: python-docs
---
## Q
`itertools.chain(a, b)` 和 `list(a) + list(b)` 都能把两个可迭代对象串起来遍历，两者在时间和空间上有什么区别？

## A
`chain(a, b)` 大致等价于对每个输入 `yield from it`：只在真正被消费到某个位置时才去取对应可迭代对象的下一个元素，不会提前把 a、b 物化（materialize）成列表再拼接，额外内存占用是 O(1)。`list(a) + list(b)` 要先把 a、b 都耗尽成完整列表、再分配一个新列表存放拼接结果，内存和 a、b 的总长度成正比，且 a、b 都必须是有限的。
