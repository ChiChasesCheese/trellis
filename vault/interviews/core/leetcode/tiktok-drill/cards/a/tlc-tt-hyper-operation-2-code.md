---
id: tlc-tt-hyper-operation-2-code
node: a.tt-hyper-operation
type: qa
step: 2
---
## Q
**手写超运算**｜写出 Python 实现

写 `hyper(n, a, b)`：`hyper(0, a, b) = b + 1`；`b = 0` 时 `hyper(1, a, 0) = a`、`hyper(2, a, 0) = 0`、`hyper(n, a, 0) = 1`（`n >= 3`）；其余 `hyper(n, a, b) = hyper(n - 1, a, hyper(n, a, b - 1))`；只允许在 `n = 0` 用 `+1`。先写直接递归版，再写把沿 `b` 的递归改成循环、递归深度不超过 `n` 的版本。

## A
**思路。** 直接递归：三条规则照抄。循环版：`hyper(n, a, b)` 是从基值出发、把 `hyper(n - 1, a, ·)` 作用 `b` 次的结果，所以沿 `b` 用 `for`，递归只剩层数 `n`。

```python
def base(n: int, a: int) -> int:
    """hyper(n, a, 0)：n=1 是 a + 0，n=2 是 a * 0，n>=3 是 1。"""
    return a if n == 1 else 0 if n == 2 else 1


def hyper(n: int, a: int, b: int) -> int:
    """直接照定义写：只有 n = 0 用 +1，其余层都由下一层构造。"""
    if n == 0:
        return b + 1
    if b == 0:
        return base(n, a)
    return hyper(n - 1, a, hyper(n, a, b - 1))


def hyper_loop(n: int, a: int, b: int) -> int:
    """递归只沿 n 走（深度 <= n），沿 b 改循环：F_n(b) = F_{n-1} 迭代 b 次，从 base 出发。"""
    if n == 0:
        return b + 1
    result = base(n, a)
    for _ in range(b):
        result = hyper_loop(n - 1, a, result)
    return result
```

运行：`hyper(1, 2, 3)`、`hyper(2, 2, 3)`、`hyper(3, 2, 3)` → `5`、`6`、`8`，对应 `2 + 3`、`2 * 3`、`2 ** 3`；`hyper(4, 2, 3)` → `16`；`[hyper(n, 2, 2) for n in range(6)]` → `[3, 4, 4, 4, 4, 4]`；`hyper(1, 2, 5000)` 在默认递归限制下 `RecursionError`，`hyper_loop(1, 2, 5000)` → `5002`；`hyper_loop(4, 2, 3)` → `16`。

**复杂度。** 直接递归：深度和调用次数都随结果大小增长，`hyper(3, 2, 3) = 8` 用 49 次调用，`hyper(3, 2, 8) = 256` 用 43707 次，`hyper(4, 2, 3) = 16` 用 203 次。`hyper_loop`：深度 `<= n`，调用次数仍随结果增长；`hyper_loop(4, 2, 4)` 的乘法层靠重复加法，调用约 `1.4 * 10^9` 次（实测 1431655884 次），要跑好几分钟，要靠闭式（见“另一种解法”）。

**写法要点。** `base` 用链式条件表达式一次给出三层的基值，避免在 `hyper` 里写三个分支；`for _ in range(b)` 里不用的循环变量写 `_`；`hyper_loop` 的循环变量 `result` 每轮喂给下一层，等价于数学上的函数迭代 `F(F(...F(base)))`；默认递归限制是 `1000`，不要靠 `sys.setrecursionlimit` 硬撑，深度问题要从算法上消掉。
