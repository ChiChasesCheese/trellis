---
id: inplace-mutation-returns-none-convention
node: model.mutability
type: qa
source: python-docs
---
## Q
`y.sort()` 和 `sorted(y)` 都能把序列排序，如果写成 `y = y.sort()` 想要一个排好序的新列表，会出什么问题？

## A
`y.sort()` 是就地排序（mutate in place），直接修改 `y` 本身并返回 `None`；`sorted(y)` 不修改原对象，返回一个新的已排序 list。标准库的约定是：凡是就地修改对象的方法一律返回 `None`，避免和「返回新对象」的操作混淆——写成 `y = y.sort()` 会让 `y` 变成 `None`，是一种容易被立刻发现的错误。
