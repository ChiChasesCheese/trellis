---
id: hl-j15-exact-missing
node: java21.j15-math-string-utils
type: qa
step: 19
---
## Q
`Math` 里没有哪些 Exact 方法？数组求和该怎么做？Exact 的异常有什么代价？

## A
没有 `powExact`、`sumExact`（数组求和）、`squareExact`。数组求和要自己在循环里用 `addExact`。

异常是**行为**，不是日志：热路径上每次溢出抛一次异常，成本大（构造栈），所以适合「溢出就是 bug / 非法输入」。需要**饱和**（超出取边界）时用 `clamp` 或手写。
