---
id: iadd-tuple-of-list-partial-mutation-trap
node: classes.operator-overloading
type: qa
source: python-docs
---
## Q
`a_tuple[i] += ['item']`（`a_tuple` 是元组，其第 `i` 个元素是一个列表）会抛 `TypeError`，但事后发现那个列表其实已经被改了——为什么会「报错了却还是生效了一部分」？

## A
`a_tuple[i] += [...]` 分两步：先算 `a_tuple[i].__iadd__(['item'])`——因为 `a_tuple[i]` 是列表，列表支持 `__iadd__()`，这一步会原地把 `'item'` 追加进那个列表并返回它自身，这一步已经真实发生、不会回滚。第二步是把这个结果重新赋回 `a_tuple[i]`，即 `a_tuple[i] = 结果`——但元组不支持给元素赋值（没有 `__setitem__`），这一步才抛出 `TypeError`。所以报错发生在第二步，但第一步的原地修改已经生效，呈现出「抛了异常但列表内容确实变了」的反直觉结果。
