---
id: hl-j15-clamp-order
node: java21.j15-math-string-utils
type: qa
step: 8
---
## Q
`Math.clamp` 的参数顺序是什么？`int` 返回的重载怎么用来限制移位量？

## A
参数顺序是 **`(value, min, max)`**，不是 `(min, max, value)`。

`(long, int, int)` 重载返回 `int`：`Math.clamp(c, 0, 32)`（`c` 是 `int`）直接给 `int`，可当移位量用，如把移位量限制到 0..32。要 `long` 结果就传三个 `long`。

需要**饱和**（saturate，超出取边界）而不是抛异常时，用 `clamp`。
