---
id: immutable-tuple-with-mutable-element
node: model.mutability
type: qa
source: python-docs
---
## Q
`t = ([1, 2],)` 这个 tuple 里存了一个 list，它算「不可变」吗？为什么这种 tuple 不能作为字典的键？

## A
tuple 本身仍是不可变的：它持有的引用集合不能改变，`t[0] = other_list` 会报错。但不可变指的是引用集合不变，不代表引用所指对象的内容不变——对 `t[0]` 这个 list 执行 `t[0].append(3)`，list 内容会变，`t` 的有效值也随之改变。因为字典键要求哈希值恒定，而这种 tuple 的哈希会依赖其内部可变对象的内容，所以它不可哈希，不能作为字典键或放入 set。
