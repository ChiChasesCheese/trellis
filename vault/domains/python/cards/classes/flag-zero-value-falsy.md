---
id: flag-zero-value-falsy
node: classes.enums
type: qa
source: python-docs
---
## Q
`IntFlag`/`Flag` 里「一个标志位都没设置」（值为 0）的成员，在布尔上下文里表现如何？这和普通 `Enum` 成员有什么不同？

## A
值为 0（没有任何标志位被设置）的 `Flag`/`IntFlag` 成员，`bool()` 求值为 `False`——比如 `Perm.R & Perm.X` 如果两者没有共同位，结果的布尔值就是 `False`，可以直接写 `if perm_result:` 判断『有没有任何位被设置』。这是 `Flag` 系列专门设计的行为；普通 `Enum` 的成员不管值是什么，作为对象本身在布尔上下文里恒为真（除非显式重写 `__bool__`），不存在『看值判断真假』这回事。
