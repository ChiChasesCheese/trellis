---
id: types-basics-optional-vs-default-arg
node: types.basics
type: qa
source: python-docs
---
## Q
`Optional[int]` 和「带默认值的可选参数」是同一个概念吗？`def foo(arg: int = 0)` 需要写成 `Optional[int]` 吗？

## A
不是同一个概念。`Optional[int]` 等价于 `int | None`（即 `Union[int, None]`，3.10 起可直接写 `X | None`），表示这个值允许显式传 `None`。而「可选参数」只是指有默认值的参数：`def foo(arg: int = 0)` 里 `arg` 可以不传，但类型仍是 `int`，不需要 `Optional`；只有当参数确实允许传入 `None` 时才该标注 `Optional[int]`，跟它有没有默认值无关。
