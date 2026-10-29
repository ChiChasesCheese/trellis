---
id: tlc-tt-hyper-operation-4-followup
node: a.tt-hyper-operation
type: qa
step: 4
---
## Q
**手写超运算**｜追问

`hyper` 的递归版和循环版写完后，面试官接着问：（1）递归深度是多少，会不会栈溢出？（2）结果规模：`hyper(4, 2, 4) = 65536`，`hyper(4, 2, 5)` 有多少位，`hyper(4, 2, 6)` 呢？（3）怎样彻底改成不递归的迭代？

## A
1. **递归深度。** 直接递归的深度随结果增长：`hyper(1, 2, 5000)` 在默认限制 `1000` 下 `RecursionError`，而答案只是 `5002`。循环版沿 `b` 不再递归，深度 `<= n`；`n` 很大时仍会溢出，`hyper_loop(5000, 2, 1)` 就是 `RecursionError`。
2. **结果规模。** `hyper(4, 2, 4) = 2 ** 16 = 65536`；`hyper(4, 2, 5) = 2 ** 65536`，有 `19729` 位十进制数字；`hyper(4, 2, 6) = 2 ** (2 ** 65536)`，仅位数就有 `2^65536` 的量级，任何机器都装不下。所以要在计算前用 `b * a.bit_length()` 估算幂的二进制位数，超过上限就抛 `OverflowError`，而不是算到内存耗尽。
3. **显式栈。** 每帧记 `[层数, 还要迭代几次, 当前值]`：栈顶这一层还要迭代时，若下一层是 `n = 0` 就直接 `+1`；否则压一帧去算 `F_{层数-1}(当前值)`；一帧迭代完，把值交给上一帧并让它的剩余次数减一。栈的深度不超过 `n`，不受递归限制影响。

```python
def hyper_stack(n: int, a: int, b: int) -> int:
    """显式栈：每帧 [层数, 还要迭代几次, 当前值]。"""
    if n == 0:
        return b + 1
    stack: list[list[int]] = [[n, b, 1 if n >= 3 else (a if n == 1 else 0)]]   # 栈底：F_n(b) 从基值出发
    while True:
        frame = stack[-1]
        level, remaining, value = frame
        if remaining == 0:                      # 这一帧算完了：值交给上一帧
            stack.pop()
            if not stack:
                return value
            parent = stack[-1]
            parent[2], parent[1] = value, parent[1] - 1
        elif level == 1:                        # 下一层是 n = 0：直接 +1
            frame[2], frame[1] = value + 1, remaining - 1
        else:                                   # 要算 F_{level-1}(value)：压一帧
            below = level - 1
            stack.append([below, value, 1 if below >= 3 else (a if below == 1 else 0)])
```

   运行：`hyper_stack(1, 2, 5000)` → `5002`，`hyper_stack(3, 2, 5)` → `32`，`hyper_stack(4, 2, 3)` → `16`，`hyper_stack(2, 7, 6)` → `42`，`hyper_stack(5000, 2, 1)` → `2`（同样的输入递归版栈溢出）。

**Python 提醒**：`len(str(x))` 数 `hyper(4, 2, 5)` 的位数会抛 `ValueError`，因为 Python 3.11 起整数转十进制字符串默认最多 `4300` 位；要么 `sys.set_int_max_str_digits(0)`，要么用 `x.bit_length() * 0.30103` 估位数。
