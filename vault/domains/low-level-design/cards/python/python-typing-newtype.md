---
id: python-typing-newtype
node: python.typing
type: qa
step: 4
tags: [grown]
---
## Q
`UserId = NewType("UserId", int)` 和直接用 `int`、或写一个 `class UserId(int)` 子类相比，区别是什么？

## A
`NewType` 在**运行时**就是一个恒等函数——`UserId(3)` 返回的还是普通的 `3`，没有任何运行时开销，也没有 `isinstance(x, UserId)` 这种检查（它不是真的子类）。它只在**类型检查器眼里**创建一个和 `int` 不兼容的新类型：函数签名要求 `UserId`，直接传一个裸 `int` 会被标红，但反过来把 `UserId` 传给要 `int` 的地方是允许的（因为它底层确实是 `int`）。价值是防止“把 `product_id` 误传进要 `user_id` 的参数”这类同类型、不同语义的参数误用，而不需要真的定义子类、付出装箱/拆箱的代价。
