---
id: tlc-fair-candy-swap-3-why
node: a.fair-candy-swap
type: qa
step: 3
---
## Q
**LC 888 公平的糖果交换**｜正确性

公平糖果交换里的 `y = x - delta` 是怎么推出来的？符号写反会错成什么样？

## A
**推导。** 交换后爱丽丝的总数是 `sumA - x + y`，鲍勃是 `sumB - y + x`。二者相等：

`sumA - x + y = sumB - y + x`，即 `2y = 2x - (sumA - sumB)`，所以 `y = x - (sumA - sumB) / 2 = x - delta`。

**不变量。** 对每个 `x`，唯一合法的 `y` 就是 `x - delta`；只要它在鲍勃的盒子里，交换就合法，否则这个 `x` 没有搭档。

**反例。** 符号写反（`x + delta`）：`aliceSizes = [1,1]`，`bobSizes = [2,2]`，`sumA = 2`，`sumB = 4`，`delta = -1`。正确 `y = 1 - (-1) = 2`，在集合里，答案 `[1,2]`；写成 `x + delta = 0` 不在集合里，最终返回 `[]`。

「保证有解」意味着 `sumA - sumB` 是偶数，所以用 `//` 取整不会丢失信息。
