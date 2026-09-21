---
id: types-gradual-narrowing-isinstance
node: types.gradual-typing
type: qa
source: python-docs
---
## Q
类型缩窄（type narrowing）最基本的手段是什么？`if isinstance(val, str): ... else: ...` 两个分支里检查器推断出的类型有什么不同？

## A
最基本的手段是在条件分支里用 `isinstance()` 做类型判定（类型谓词，type predicate）。例如对 `val: str | float`，`if isinstance(val, str):` 分支内 `val` 被缩窄为 `str`，对应的 `else` 分支被缩窄为 `float`；缩窄只在该分支作用域内成立，离开分支后类型恢复为原始的联合类型。
