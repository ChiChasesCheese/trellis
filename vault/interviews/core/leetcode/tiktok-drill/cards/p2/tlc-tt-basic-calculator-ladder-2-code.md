---
id: tlc-tt-basic-calculator-ladder-2-code
node: p2.tt-basic-calculator-ladder
type: qa
step: 2
---
## Q
**计算器梯度题（先校验再求值）**｜写出 Python 实现

写 `is_valid(s) -> bool` 和 `calculate(s) -> int`：表达式含非负整数、`+ - * /`、括号和空格，除法向零取整，一元负号只出现在开头或 `(` 之后；`1 <= len(s) <= 3 * 10^5`。`is_valid` 对空串、非法字符、括号不配对、连续运算符、缺操作数返回 `False`；`calculate` 在不合法时抛 `ValueError`。

## A
**思路。** `tokenize` 用正则一次切成数字和符号；`is_valid` 用「期待操作数 / 期待运算符」加括号深度扫一遍；`calculate` 用数字栈和运算符栈，栈顶优先级不低于新运算符就先算（同级左结合），一元负号补 `0`。

```python
import re

PREC = {"+": 1, "-": 1, "*": 2, "/": 2}
TOKEN = re.compile(r"\s*(?:(\d+)|(\S))")


def tokenize(s: str) -> list[int | str]:
    """数字变成 int，其余单字符原样保留；遇到非法字符抛 ValueError。"""
    tokens: list[int | str] = []
    for m in TOKEN.finditer(s):
        num, ch = m.groups()
        if num is not None:
            tokens.append(int(num))
        elif ch in "+-*/()":
            tokens.append(ch)
        else:
            raise ValueError(f"illegal character {ch!r}")
    return tokens


def is_valid(s: str) -> bool:
    """先校验：空串、非法字符、括号不配对、连续运算符、缺操作数都返回 False。
    一元负号只允许出现在表达式开头或 '(' 之后。"""
    try:
        tokens = tokenize(s)
    except ValueError:
        return False
    depth, want_operand, prev = 0, True, None
    for tok in tokens:
        if want_operand:
            if isinstance(tok, int):
                want_operand = False
            elif tok == "(":
                depth += 1
            elif tok == "-" and prev in (None, "("):
                pass                                  # 一元负号，后面仍然需要操作数
            else:
                return False
        else:
            if tok == ")":
                depth -= 1
                if depth < 0:
                    return False
            elif tok in PREC:
                want_operand = True
            else:
                return False
        prev = tok
    return bool(tokens) and not want_operand and depth == 0


def _apply(op: str, a: int, b: int) -> int:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    q = abs(a) // abs(b)                              # 整数除法向零取整：不能直接用 //（向下取整）
    return q if (a < 0) == (b < 0) else -q


def calculate(s: str) -> int:
    if not is_valid(s):
        raise ValueError("invalid expression")
    nums: list[int] = []
    ops: list[str] = []

    def reduce_top() -> None:
        b, a = nums.pop(), nums.pop()
        nums.append(_apply(ops.pop(), a, b))

    prev = None
    for tok in tokenize(s):
        if isinstance(tok, int):
            nums.append(tok)
        elif tok == "(":
            ops.append(tok)
        elif tok == ")":
            while ops[-1] != "(":
                reduce_top()
            ops.pop()
        else:
            if tok == "-" and prev in (None, "("):
                nums.append(0)                         # 一元负号：补一个 0，变成 0 - x
            while ops and ops[-1] != "(" and PREC[ops[-1]] >= PREC[tok]:
                reduce_top()                           # 同级左结合：先算左边
            ops.append(tok)
        prev = tok
    while ops:
        reduce_top()
    return nums[0]
```

运行：`"3+2*2"` → `7`，`" 3/2 "` → `1`，`" 3+5 / 2 "` → `5`，`"14-3/2"` → `13`，`"(1+(4+5+2)-3)+(6+8)"` → `23`，`"-(2+3)"` → `-5`，`"(-7)/2"` → `-3`，`"-2*3"` → `-6`；`is_valid("")`、`is_valid("1+")`、`is_valid("(1+2")`、`is_valid("1++2")`、`is_valid("2*-3")`、`is_valid("()")` 都是 `False`，`is_valid("(-1)")` 是 `True`；嵌套 `10^5` 层括号的表达式不到 `0.1` 秒算完。

**复杂度。** 时间 `O(n)`：每个 token 至多进出栈一次；空间 `O(n)`。

**写法要点。**
- `re.compile(r"\s*(?:(\d+)|(\S))")` 配 `finditer`：一次切出数字和符号，跳过空白，不手写字符循环；两个捕获组里恰有一个非 `None`，用它区分。
- `isinstance(tok, int)` 区分数字和符号：token 列表混放 `int` 和 `str`，类型本身就是标签。
- `_apply` 里的向零取整：`abs(a) // abs(b)` 再按符号还原；`int(a / b)` 走浮点数，过大会丢精度。
- `prev in (None, "(")` 判断「开头或 `(` 之后」，校验和求值共用这一个条件。
