---
id: cc-python-pitfalls-shallow-copy
node: python.pitfalls
type: qa
---
## Q
`grid = [ [0] * 3 ] * 3; grid[0][0] = 1` sets three cells. And `b = dict(a)` still lets you corrupt `a`. Explain both, and give the fixes.

## A
**`*` and `dict()` / `list()` copy *references*, one level deep.**

- `[ [0] * 3 ] * 3` makes three references to one row object. Build it with a comprehension: `[ [0] * 3 for _ in range(3) ]`.
- `b = dict(a)` is a new dict whose values are the *same* objects, so `b[k].append(x)` mutates `a[k]`. Use `copy.deepcopy(a)`, or better, stop sharing mutable values.
- Related identity trap: `copy.copy(x) == x` is `True` but `copy.copy(x) is x` is `False`. `is` tests identity, `==` tests value. Small ints and short strings are cached so `is` appears to work and then stops — reserve `is` for `None`, `True` and `False`.

## Q zh
`grid = [ [0] * 3 ] * 3; grid[0][0] = 1` 会设置三个格子。而 `b = dict(a)` 之后你仍能破坏 `a`。解释这两件事，并给出修法。

## A zh
**`*` 和 `dict()` / `list()` 复制的是*引用*，只有一层。**

- `[ [0] * 3 ] * 3` 造出的是指向同一个行对象的三个引用。用推导式构造：`[ [0] * 3 for _ in range(3) ]`。
- `b = dict(a)` 是一个新字典，但值还是*同一批*对象，所以 `b[k].append(x)` 会改到 `a[k]`。用 `copy.deepcopy(a)`，更好的做法是不要共享可变值。
- 相关的同一性陷阱：`copy.copy(x) == x` 为 `True`，但 `copy.copy(x) is x` 为 `False`。`is` 比较同一性，`==` 比较值。小整数和短字符串会被缓存，于是 `is` 看起来能用、然后突然不能用 —— 把 `is` 留给 `None`、`True` 和 `False`。
