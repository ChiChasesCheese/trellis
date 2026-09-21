---
id: containers-timsort-minrun
node: performance.containers
type: qa
source: cpython-internals
---
## Q
Timsort 处理长度小于 minrun（一个 32～64 之间的 2 的幂）的天然 run 时会怎么做？为什么 minrun 要挑在这个区间，而不是更小或更大？

## A
会用二分插入排序（binary insertion sort）把这段人为补齐到 minrun 长度再参与合并，保证参与合并的 run 都不会太短。minrun 太小（如 8）会让函数调用次数和合并趟数暴增，太大（如 256）会让二分插入排序本身的数据搬移成本变高，32～64 是两者的折中。
