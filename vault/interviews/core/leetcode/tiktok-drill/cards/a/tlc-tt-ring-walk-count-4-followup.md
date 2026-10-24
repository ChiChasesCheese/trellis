---
id: tlc-tt-ring-walk-count-4-followup
node: a.tt-ring-walk-count
type: qa
step: 4
---
## Q
**圆环上走 n 步回到原点的方案数**｜追问

环上 `10` 个点，恰好 `n` 步回到点 `0` 的方案数，已经用 `O(10n)` 的滚动数组解决。面试官接着问：（1）`n` 达到 `10^18` 怎么办？（2）有没有公式？（3）终点不是 `0`，或者有些点是障碍？

## A
1. **`n` 极大**：一步的转移是固定的 `10 x 10` 矩阵（相邻点为 `1`），`n` 步就是矩阵的 `n` 次幂，用快速幂 `O(10^3 · log n)`。

```python
def ring_walks_matrix(n: int, size: int = 10, mod: int = 10**9 + 7) -> int:
    def mul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
        return [[sum(x * y for x, y in zip(row, col)) % mod for col in zip(*b)] for row in a]

    step = [[int(j in ((i - 1) % size, (i + 1) % size)) for j in range(size)] for i in range(size)]
    result = [[int(i == j) for j in range(size)] for i in range(size)]
    while n:
        if n & 1:
            result = mul(result, step)
        step = mul(step, step)
        n >>= 1
    return result[0][0]
```

   `n = 100000` 与滚动数组都是 `131065086`，`n = 10**18` → `804027789`。
2. **公式**：顺时针 `j` 步、逆时针 `n - j` 步，净位移 `2j - n` 必须是 `10` 的倍数，答案是对所有满足条件的 `j` 求 `C(n, j)` 之和，`n = 10` 时是 `1 + 252 + 1 = 254`。`n` 大时要预处理阶乘和逆元，`O(n)`。
3. **其他终点或障碍**：答案取 `ways[target]`；障碍点在每步更新后把 `ways[blocked]` 置零；环的点数 `size` 是参数，步长可选就多加几项转移。

**Python 提醒**：矩阵乘法里 `zip(*b)` 把列取出来，`sum(x * y for ...)` 在取模前可能很大，Python 整数不会溢出但要及时 `% mod`；`math.comb(n, j)` 是精确大整数，`n` 到 `10^5` 时每一项很大，求和前不取模会很慢。
