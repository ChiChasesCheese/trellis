---
id: c3-linearization-formula
node: classes.inheritance-mro
type: cloze
source: python-docs
---
C3 算法给出类 `C(B1, B2, ..., BN)` 的方法解析顺序（method resolution order，MRO）公式：`L[C] = C + merge({{c1::L[B1], L[B2], ..., L[BN]}}, {{c2::B1, B2, ..., BN}})`，其中 `merge` 每一步从各列表的表头里选一个「{{c3::不出现在任何列表尾部（tail）中}}」的类，加入结果并从所有列表里删除它，选不出这样的表头就说明层级本身有冲突。
