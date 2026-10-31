---
id: tlc-climbing-stairs-2-code
node: b.climbing-stairs
type: qa
step: 2
---
## Q
**LC 70 爬楼梯**｜写出 Python 实现

`n` 阶楼梯（`1 <= n <= 45`），每次爬 `1` 或 `2` 阶，返回到达楼顶的不同方法数。要求 `O(n)` 时间、`O(1)` 空间。

## A
**思路。** `f(k) = f(k-1) + f(k-2)`，初值 `f(0) = 1`、`f(1) = 1`；只保留最近两项，循环 `n - 1` 次推到 `f(n)`。

```python
def climb_stairs(n: int) -> int:
    prev, cur = 1, 1                   # f(0) = 1（站着不动算一种），f(1) = 1
    for _ in range(n - 1):
        prev, cur = cur, prev + cur    # f(k) = f(k-1) + f(k-2)：最后一步迈 1 阶或 2 阶
    return cur
```

运行：`n = 1` → `1`，`n = 2` → `2`，`n = 3` → `3`，`n = 1..10` → `1, 2, 3, 5, 8, 13, 21, 34, 55, 89`，`n = 45` → `1836311903`。

**复杂度。** 时间 `O(n)`：循环 `n - 1` 次；空间 `O(1)`：两个变量。

**写法要点。** `prev, cur = cur, prev + cur` 是元组赋值，右边先整体算完再赋值，所以不需要临时变量。`for _ in range(n - 1)` 里 `_` 表示不用循环变量。`n = 1` 时 `range(0)` 为空，直接返回 `cur = 1`，不需要单独写 `if n <= 2`。Python 的整数没有上限，不用担心溢出，换成 Java / C++ 要注意 `n = 45` 已接近 `int32` 上限。
