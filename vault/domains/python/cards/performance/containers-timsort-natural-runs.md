---
id: containers-timsort-natural-runs
node: performance.containers
type: qa
source: cpython-internals
---
## Q
CPython 的排序算法 Timsort 为什么被称为「自适应」（adaptive）？它是怎么利用输入里已经有序的部分的？

## A
Timsort 从左到右扫描数组，先识别出一段段天然的「run」——连续非降序或非升序的子序列（降序段会原地反转成升序），再把这些 run 两两合并成更大的有序段。数据里已经有序的段落越长，需要的合并和比较就越少，因此在接近有序的真实数据上比纯随机数据快得多，同时保证稳定（相等元素相对顺序不变）。
