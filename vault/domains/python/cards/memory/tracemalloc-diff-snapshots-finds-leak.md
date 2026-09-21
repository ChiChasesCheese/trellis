---
id: tracemalloc-diff-snapshots-finds-leak
node: memory.leaks-tracemalloc
type: qa
source: python-docs
---
## Q
用 `tracemalloc` 定位内存泄漏时，为什么要在「怀疑泄漏的操作前后」各拍一次快照（snapshot），而不是只看一次快照的 Top N？

## A
单次快照的 Top N 只能看出「谁现在占用内存最多」，分不清是正常的长期占用还是泄漏；用 `snapshot2.compare_to(snapshot1, 'lineno')` 对比两次快照，能直接列出两次之间「新增了多少内存、新增了多少个内存块」，按分配位置（文件名+行号）排序，泄漏点通常就是差值（diff）最大的那几行。
