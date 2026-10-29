---
id: tlc-tt-hyper-operation-5-alt
node: a.tt-hyper-operation
type: qa
step: 5
---
## Q
**手写超运算**｜另一种解法

`hyper_loop` 在乘法层靠重复加法，`hyper(4, 2, 4)` 的调用次数达到 `10^9` 量级，算不出来。有没有办法让 `hyper(4, 2, 4)` 和 `hyper(4, 2, 5)` 瞬间得到结果？什么时候用它，什么时候保留“只允许用 `+1`”的纯递归版？

## A
**思路：前三层用内置运算。** 层 `1`、`2`、`3` 有闭式 `a + b`、`a * b`、`a ** b`，Python 的大整数做乘法和快速幂（`O(log b)` 次乘法）都很快。只有 `n >= 4` 才需要真正迭代，每轮把上一层的结果当作下一轮的指数。计算前估算幂的位数，超过上限就拒绝。

```python
MAX_BITS = 10_000_000                           # 结果超过一千万位二进制就拒绝计算


def hyper_fast(n: int, a: int, b: int) -> int:
    """n <= 3 用内置运算（加、乘、快速幂）；n >= 4 才迭代，并在结果过大时拒绝。"""
    if n == 0:
        return b + 1
    if n == 1:
        return a + b
    if n == 2:
        return a * b
    if n == 3:
        if a > 1 and b * a.bit_length() > MAX_BITS:
            raise OverflowError("结果太大")
        return a ** b
    result = 1                                  # n >= 4：b = 0 时是 1
    for _ in range(b):
        result = hyper_fast(n - 1, a, result)
    return result
```

运行：`[hyper_fast(4, 2, b) for b in range(5)]` → `[1, 2, 4, 16, 65536]`；`hyper_fast(4, 2, 5)` 的二进制位数是 `65537`、十进制位数是 `19729`；`hyper_fast(4, 3, 3)` → `7625597484987`（`3^27`）；`hyper_fast(5, 2, 1)` → `2`；`hyper_fast(4, 2, 6)` → `OverflowError`。

**什么时候用哪个。**
- 面试要求“只允许在 `n = 0` 用 `+1`”：写直接递归版，再说明深度和规模；这版只能算很小的数，但完全对应定义。
- 要真正算 `hyper(4, 2, 4)`、`hyper(4, 2, 5)` 这类塔：用闭式版，层 `1` 到 `3` 交给内置运算，层 `4` 起迭代，并设位数上限。
- 要处理很大的层数 `n`：循环版 + 显式栈，递归深度不再受限。

闭式版的代价是不再体现“每层由下一层构造”，所以先写递归版，再提这个优化。
