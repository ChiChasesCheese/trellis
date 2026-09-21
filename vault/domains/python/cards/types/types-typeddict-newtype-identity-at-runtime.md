---
id: types-typeddict-newtype-identity-at-runtime
node: types.typeddict-literal
type: qa
source: python-docs
---
## Q
`UserId = NewType('UserId', int)` 之后，`UserId(524313)` 在运行时到底做了什么？`UserId` 能被继续子类化吗？

## A
`NewType` 在运行时只生成一个可调用对象，调用它会原样返回传入的参数——`some_value is UserId(some_value)` 恒成立，没有创建新类，也几乎没有额外开销。它的作用完全是给静态检查器看的：检查器把 `UserId` 当成 `int` 的子类型，`UserId(-1)` 这种直接构造能通过检查，但把裸 `int` 传给期望 `UserId` 的参数会报错，用来防止把不同语义的同底类型（如订单 id 和用户 id，都是 `int`）混用。`UserId` 不允许被继续子类化，比如 `class AdminUserId(UserId)` 在运行时直接失败。
