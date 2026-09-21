---
id: missing-contains-degrades-to-linear-scan
node: model.dunder-protocols
type: qa
source: python-docs
---
## Q
一个容器类没有实现 `__contains__`，只实现了 `__iter__`，用 `in` 运算符做成员测试时会有什么性能代价？

## A
没有 `__contains__` 时，`in`/`not in` 会退化为遍历：先尝试用 `__iter__()` 逐个取出元素比较，连 `__iter__` 也没有的话再退到更旧的 `__getitem__` 循环协议，直到抛出 `IndexError` 才停止。这意味着每次成员测试都是 O(n) 的线性扫描；如果容器内部本可以用哈希表或索引做到更快查找，不实现 `__contains__` 就放弃了这个优化，退化成暴力遍历。
