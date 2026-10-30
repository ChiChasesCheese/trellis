---
id: uth-python-numbers-floats-5-floordiv
node: python.numbers-floats
type: qa
step: 5
---
## Q
**-7 // 2 为什么是 -4**｜Python · CPython 3.14

C++、Java 里 `-7 / 2` 是 `-3`，Python 里 `-7 // 2` 却是 `-4`；`-7 % 3` 是 `2`，不是 `-1`。为什么不一样？

## A
**背景。** 除不尽时，要决定商往哪边舍：向零截断（-3.5 变 -3），或向下取整（-3.5 变 -4）。余数跟着商走，才能让「被除数 = 商 × 除数 + 余数」恒成立。

**结构。** Python 的 `//` 向下取整，`%` 的结果和除数同号，两者满足 `x == (x // y) * y + x % y`。CPython 先做 C 风格的截断除法，若余数与除数异号，就把余数加一个除数、商减 1。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<line x1="20" y1="74" x2="320" y2="74" stroke-width="1.2" stroke="currentColor"/>
<line x1="60" y1="68" x2="60" y2="80" stroke-width="1.2" stroke="currentColor"/>
<text x="60" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-4</text>
<line x1="160" y1="68" x2="160" y2="80" stroke-width="1.2" stroke="currentColor"/>
<text x="160" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-3</text>
<line x1="260" y1="68" x2="260" y2="80" stroke-width="1.2" stroke="currentColor"/>
<text x="260" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-2</text>
<circle cx="110" cy="74" r="5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<line x1="110" y1="56" x2="70.0" y2="56.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="64,56 70.0,53.0 70.0,59.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="110" y1="56" x2="150.0" y2="56.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="156,56 150.0,59.0 150.0,53.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="78" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">// 向下 -4</text>
<text x="160" y="40" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">C 向零 -3</text>
<text x="110" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-7 / 2 = -3.5</text>
<text x="170" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">负数时两种取整差 1</text>
</svg>
```

| 表达式 | Python | C++ / Java / Go / Rust |
|---|---|---|
| `-7 // 2`（C 系写 `-7 / 2`） | `-4` | `-3` |
| `-7 % 3` | `2` | `-1` |
| `7 % -3` | `-2` | `1` |

**为什么。** 除数为正时，`x % n` 永远落在 0 到 n−1：环形下标 `(i - 1) % n` 不用再手动补 `+ n`。

**坑。** 想要向零截断，要写 `int(a / b)`，不能写 `//`；`math.fmod` 给的是 C 风格的余数（和被除数同号）。

**例题：** LC 150 逆波兰表达式求值（同类：LC 227 基本计算器 II）

计算后缀表达式 `tokens` 的值，运算符有 `+ - * /`，整数除法向零截断。例：`["4","13","5","/","+"]` → `6`；`["10","6","9","3","+","-11","*","/","*","17","+","5","+"]` → `22`。

```python
def eval_rpn(tokens: list[str]) -> int:
    stack: list[int] = []
    ops = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: int(a / b),
    }
    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    return stack[0]
```
