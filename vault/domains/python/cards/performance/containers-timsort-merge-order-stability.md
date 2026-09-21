---
id: containers-timsort-merge-order-stability
node: performance.containers
type: qa
source: cpython-internals
---
## Q
Timsort 合并三个相邻的有序 run A、B、C 时，为什么不能先合并 A 和 C（哪怕这样计算上更省事）？

## A
Timsort 要保证排序稳定（stable）：相等的元素必须保持它们在原数组里的相对顺序。如果 A、B、C 中出现相同的元素，先合并 A 和 C 会打乱它们相对 B 中同值元素的先后关系，所以合并只能按相邻顺序做，即 (A+B)+C 或 A+(B+C)，从不跳着合并。
