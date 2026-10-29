---
id: tlc-tt-hyper-operation-0-whole
node: a.tt-hyper-operation
type: qa
---
## Q
**手写超运算**｜Hard · TikTok 高频

实现超运算 `hyper(n, a, b)`（`n`、`a`、`b` 为非负整数，`n <= 5`，输入保证结果在可计算范围内）。`n = 0` 是后继 `b + 1`；`n = 1` 是加法 `a + b`；`n = 2` 是乘法 `a * b`；`n = 3` 是幂 `a ** b`；`n >= 4` 是迭代幂（`a` 的 `b` 层塔）。统一的定义只有三条：`n = 0` 时 `hyper(0, a, b) = b + 1`；`b = 0` 时 `hyper(1, a, 0) = a`、`hyper(2, a, 0) = 0`、`hyper(n, a, 0) = 1`（`n >= 3`）；其余 `hyper(n, a, b) = hyper(n - 1, a, hyper(n, a, b - 1))`。只允许在 `n = 0` 用 `+1`，其余层都要由下一层构造出来。

先给递归写法，再讨论递归深度、结果规模和怎样改成迭代。例：`hyper(3, 2, 3) = 8`，`hyper(4, 2, 3) = 16`，`hyper(4, 2, 4) = 65536`，`hyper(4, 2, 5)` 有 19729 位十进制数字。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 三条规则照抄成递归：`n = 0` 返回 `b + 1`；`b = 0` 返回该层的基值（`a`、`0`、`1`）；否则 `hyper(n - 1, a, hyper(n, a, b - 1))`。每一层都是“把下一层迭代 `b` 次”：加法是 `+1` 做 `b` 次，乘法是 `+a` 做 `b` 次，幂是 `*a` 做 `b` 次，迭代幂是 `a **` 做 `b` 次。实用写法：递归只沿层数 `n` 走，沿 `b` 改循环，`n <= 3` 直接用内置运算，并给结果规模设上限。

**识别。** 「每层由下一层构造」「嵌套递归，自变量里又调用自己」是阿克曼函数（Ackermann function）一类的定义：增长比指数快得多，所以考点不在算法技巧，而在**读懂定义**、写对基值（`b = 0` 的值每层不同）、说清递归深度和结果规模。

**推导。** 直接递归：`hyper(1, a, b)` 展开成 `hyper(0, a, hyper(1, a, b - 1))`，沿 `b` 的递归深度是 `b`，`hyper(1, 2, 5000)` 就栈溢出，而答案只是 `5002`；乘法层是加法层 `b` 次，调用次数随结果增长，`hyper(3, 2, 8) = 256` 已经要 43707 次调用。浪费：沿 `b` 的递归其实是循环——`hyper(n, a, b)` 就是从基值出发，把 `hyper(n - 1, a, ·)` 作用 `b` 次，改成 `for` 循环后递归只剩 `n` 层。再进一步：层 `1` 到 `3` 有闭式（`a + b`、`a * b`、`a ** b`），Python 的大整数运算直接算，只有 `n >= 4` 才需要真正迭代，`hyper(4, 2, 5)` 瞬间得到；塔高再加一层，`hyper(4, 2, 6)` 就是 `2 ** (2 ** 65536)`，光是位数就有 `2^65536` 的量级，无法表示，要在计算前估算大小并拒绝。

```python
MAX_BITS = 10_000_000                           # 结果超过一千万位二进制就拒绝计算


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

运行：`hyper(3, 2, 3)` → `8`，`hyper(4, 2, 3)` → `16`，`hyper(2, 2, 100)` → `200`；`hyper(1, 2, 5000)` 在默认递归限制下 `RecursionError`，`hyper_loop(1, 2, 5000)` → `5002`；`[hyper_fast(4, 2, b) for b in range(5)]` → `[1, 2, 4, 16, 65536]`；`hyper_fast(4, 2, 5)` 有 `19729` 位十进制数字；`hyper_fast(4, 3, 3)` → `7625597484987`（即 `3^27`）；`hyper_fast(4, 2, 6)` → `OverflowError`。

**复杂度。** 直接递归的深度和调用次数都随结果大小增长（`hyper(3, 2, 3) = 8` 用 49 次调用，`hyper(3, 2, 8) = 256` 用 43707 次）；`hyper_loop` 深度 `<= n`，时间仍随结果增长；`hyper_fast` 的 `n <= 3` 是 `O(1)` 次大整数运算（幂 `O(M(b·log a))`，`M` 是乘法代价），`n >= 4` 时的循环只有 `b` 轮，成本由最后一层的大整数幂决定。

**易错点。**
- 基值写错：`b = 0` 时每层不同。全取 `1`：`hyper(1, 3, 4)` 得 `5`（应 `7`），`hyper(2, 3, 4)` 得 `5`（应 `12`），`hyper(3, 2, 3)` 得 `4`（应 `8`）；`n >= 3` 取 `0`：`hyper(3, 2, 3)` 得 `0`（应 `8`）。
- `a = 0` 的塔：`hyper(4, 0, b)` 对 `b = 0, 1, 2, 3, 4, 5` 依次是 `1, 0, 1, 0, 1, 0`，因为 `0 ** 0 = 1`；自己写快速幂时要把 `0 ** 0` 当作 `1`。
- `len(str(x))` 数位数：`hyper(4, 2, 5)` 有 19729 位，超过 Python 默认的 4300 位转换上限，直接抛 `ValueError`；估大小用 `x.bit_length()`。

**追问。**
- 递归深度：直接递归的深度随值增长；`hyper_loop` 只剩 `n` 层，`hyper_loop(5000, 2, 1)` 仍栈溢出，需要显式栈。
- 结果规模：塔高每加一层，数值变成 `a` 的“上一个结果”次方；先估大小再算，超限就拒绝。
- 改迭代：循环化 `b`；彻底不用递归就用显式栈，每帧记 `[层数, 还剩几次, 当前值]`。

**同模式。** LC 50 快速幂、LC 372 超级次方（幂的幂）、LC 43 字符串相乘（乘法拆成加法）、LC 29 两数相除（用加减法实现除法）；阿克曼函数是同一类嵌套递归定义。
