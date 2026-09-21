---
id: str-bytes-hash-salted-random
node: model.hash-eq
type: qa
source: python-docs
---
## Q
为什么同一个字符串在两次不同的 Python 进程运行里，`hash()` 的结果可能不一样？这样设计是为了防什么？

## A
从 Python 3.3 起，`str` 和 `bytes` 的哈希值默认会加入一个每次进程启动时随机生成的「盐」（salted），在同一个进程内保持稳定，但跨进程不可预测。这是为了防御一种拒绝服务攻击：攻击者精心构造大量哈希值相同的字符串作为 dict 的键，如果哈希算法固定可预测，插入这些键会触发大量哈希冲突，让 dict 插入退化到 O(n²) 的最坏情况；加盐后攻击者无法提前算出会冲突的输入。副作用是 set 的遍历顺序也依赖这个随机哈希，Python 从不保证 set 遍历顺序。
