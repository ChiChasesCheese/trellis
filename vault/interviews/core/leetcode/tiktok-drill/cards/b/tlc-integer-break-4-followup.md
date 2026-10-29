---
id: tlc-integer-break-4-followup
node: b.integer-break
type: qa
step: 4
---
## Q
**LC 343 整数拆分**｜Medium · 字节高频｜追问

面试官接着问：（1）能不能 `O(1)`，为什么是 `3`？（2）`n` 到 `10^9`，结果对 `10^9 + 7` 取模？（3）要把具体的拆分方案也输出？

## A
1. **数学解**：每个因子 `x >= 5` 都可以拆成 `3 + (x - 3)`，而 `3 * (x - 3) > x`，所以最优解里没有 `>= 5` 的数；`4 = 2 + 2` 乘积不变，`1` 只会让乘积不增。至多留两个 `2`（`2 * 2 * 2 = 8 < 3 * 3 = 9`）。结果：
```python
def integer_break_math(n: int) -> int:
    if n <= 3:
        return n - 1
    q, r = divmod(n, 3)
    if r == 0:
        return 3 ** q
    return 3 ** (q - 1) * 4 if r == 1 else 3 ** q * 2
```
2. **大 `n` 取模**：`3 ** q` 换成 `pow(3, q, MOD)`，`O(log n)`，`n = 10^9` 时余 `1`，答案是 `pow(3, q - 1, MOD) * 4 % MOD`。DP 版的 `O(n^2)` 不可用。
3. **输出方案**：DP 里同时存下取到最大值的 `j`，从 `n` 往回跳；或者直接按数学解输出 `q` 个 `3` 加上余数部分。

**Python 提醒**：`divmod(n, 3)` 一次拿商和余数；`3 ** q` 在 Python 里是任意精度整数，不会溢出，但很大时要用三参数 `pow` 控制规模。
