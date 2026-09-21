---
id: tee-buffers-gap-between-branches
node: iteration.itertools
type: qa
source: python-docs
---
## Q
用 `it1, it2 = itertools.tee(it, 2)` 把一个迭代器拆成两份后，如果 it1 一路遍历到底而 it2 迟迟不动，会有什么代价？什么情况下直接用 `list(it)` 比 `tee` 更划算？

## A
`tee` 内部要把两个分支「进度差」之间的元素暂存起来等慢分支来取：快分支领先慢分支越多，`tee` 占用的辅助存储（auxiliary storage）就越大，最坏情况下相当于把整个序列都缓存了一份，并没有省内存。如果本来就知道会有一个分支几乎把数据读完、另一个分支才刚开始，直接用 `list(it)` 物化一次、两个分支各自独立遍历这份 list，通常比 `tee` 更快也更省心。
