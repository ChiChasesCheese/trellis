---
id: tlc-tt-basic-calculator-ladder-0-whole
node: p2.tt-basic-calculator-ladder
type: qa
---
## Q
**计算器梯度题（先校验再求值）**｜Hard · 近一年被问：美国 6 次、国内 2 次 · 最近 2026-09-09（美国面试记录）

给一个字符串表达式 `s`，实现整数计算器 `calculate(s)`。面试官逐级加条件：（1）只有 `+ - * /` 和空格，没有括号，要处理优先级，除法是整数除法（向零取整）；（2）再加括号和一元负号；（3）先校验表达式是否合法（空串、非法字符、括号不配对、连续运算符、缺操作数），合法才计算。`1 <= len(s) <= 3 * 10^5`，操作数是非负整数；一元负号只出现在表达式开头或 `(` 之后；除数不会是 `0`。例：`"3+2*2"` → `7`，`" 3/2 "` → `1`，`"(1+(4+5+2)-3)+(6+8)"` → `23`，`"-(2+3)"` → `-5`，`"2*-3"` 不合法。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先过一遍状态机校验（「现在该出现操作数还是运算符」加括号深度），再用双栈（数字栈、运算符栈）求值：遇到运算符先把栈顶优先级不低于它的运算符算掉（同级左结合），`(` 当隔板，`)` 把括号内算完；一元负号补一个 `0`，变成 `0 - x`。`O(n)` 时间、`O(n)` 空间，全部迭代，括号嵌套再深也不会爆栈。

**识别。** 有优先级和括号的表达式求值是栈的经典题：运算符栈保存「还没轮到算」的运算符。`3 * 10^5` 的长度和任意深的括号意味着递归下降（recursive descent）会 `RecursionError`，用显式栈。「先校验」就是让同一个「期待操作数 / 期待运算符」的状态机先跑一遍，错误在算之前就拦住。

**推导。** 暴力：反复找最内层括号，把括号内的子串算出来替换回去，每次都重扫整个字符串，`O(n^2)`。浪费：同一段被反复扫描。洞察：优先级决定「能不能现在算」——栈顶运算符优先级不低于新来的，它的两个操作数都已就绪，立刻算；否则新运算符先入栈等右操作数。括号用 `(` 当栈里的隔板。每个数字、运算符各进出栈一次，`O(n)`。一元负号只有在开头和 `(` 之后出现，补一个 `0`，不需要专门的一元运算符。

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

运行：`"3+2*2"` → `7`，`" 3/2 "` → `1`，`" 3+5 / 2 "` → `5`，`"14-3/2"` → `13`，`"(1+(4+5+2)-3)+(6+8)"` → `23`，`"-(2+3)"` → `-5`，`"(-7)/2"` → `-3`，`"-2*3"` → `-6`，`"2*(5+5*2)/3+(6/2+8)"` → `21`；`is_valid` 对 `""`、`"1+"`、`"(1+2"`、`"1+2)"`、`"1++2"`、`"2*-3"`、`"()"`、`"1 2"`、`"a+1"` 都返回 `False`，对 `"(-1)"`、`"-(-1)"` 返回 `True`；`"(" * 100000 + "1" + "+1)" * 100000`（嵌套 `10^5` 层）→ `100001`，不到 `0.1` 秒。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（两个栈和 token 列表）。

**易错点。**
- 同级要左结合：弹出条件写成 `>`，`"8-3-2"` 得到 `7`，`"8/4/2"` 得到 `4`；正确是 `3` 和 `1`（条件是 `>=`）。
- 整数除法向零取整：直接用 `//` 向下取整，`"(-7)/2"` 得到 `-4`，正确是 `-3`；也不能用 `int(a / b)`，浮点数在 `10^17` 以上丢精度（`int(10**17 / 3)` 是 `33333333333333332`，正确是 `33333333333333333`）。
- 一元负号：不补 `0`，`"-(2+3)"` 和 `"(-1)+2"` 都会 `IndexError`。
- 不校验会静默出错：去掉校验后 `"1 2"` 返回 `1`，`"2*-3"`、`"()"`、`"1+"` 都抛 `IndexError`，该给出的是明确的 `ValueError`。

**追问。**
- 输入是字符数组 `list[str]`：`"".join(chars)` 一次 `O(n)` 就能复用；要求不额外建字符串时，改成直接遍历字符。
- 测试：空串、纯空格、单个数、开头 `-`、嵌套 `10^5` 层、负数除法、连续运算符、与 Python `eval`（只含 `+ - *` 和括号时）对照。
- 加 `^`（右结合）、小数、变量：换一张优先级表；右结合的弹出条件改成 `>`，其他结构不变。

**同模式。** LC 227 基本计算器 II、LC 224 基本计算器、LC 772 基本计算器 III、LC 150 逆波兰表达式求值、LC 394 字符串解码。
