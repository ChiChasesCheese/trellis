---
slug: tt-basic-calculator-ladder
---
## Q
**计算器梯度题（先校验再求值）**｜Hard

实现 `calculate(s)`：支持 `+ - * /`（整数除法向零取整）、括号、一元负号（只出现在开头或 `(` 之后）、空格；先校验表达式合法（空串、非法字符、括号不配对、连续运算符、缺操作数），合法才求值。

## A
**一句话。** 先用「该出现操作数还是运算符」加括号深度的状态机校验，再用数字栈和运算符栈求值，一元负号补 `0`。

```python
PREC = {"+": 1, "-": 1, "*": 2, "/": 2}
TOKEN = re.compile(r"(\d+)|(\S)")

def tokenize(s):
    toks = []
    for m in TOKEN.finditer(s):
        num, ch = m.groups()
        if num is not None:
            toks.append(int(num))
        elif ch in "+-*/()":
            toks.append(ch)
        else:
            raise ValueError(ch)     # 非法字符
    return toks

def is_valid(s):
    try:
        toks = tokenize(s)
    except ValueError:
        return False
    depth, want, prev = 0, True, None   # want：现在该出现操作数
    for t in toks:
        if want:
            if isinstance(t, int):
                want = False
            elif t == "(":
                depth += 1
            elif not (t == "-" and prev in (None, "(")):
                return False        # 只有一元负号可以不是操作数
        elif t == ")":
            depth -= 1
            if depth < 0:
                return False
        elif t in PREC:
            want = True
        else:
            return False
        prev = t
    return bool(toks) and not want and depth == 0

def apply(op, a, b):
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    q = abs(a) // abs(b)            # 向零取整，不能直接 //
    return q if (a < 0) == (b < 0) else -q

def calculate(s):
    if not is_valid(s):
        raise ValueError("invalid expression")
    nums, ops = [], []
    def reduce():
        b, a = nums.pop(), nums.pop()
        nums.append(apply(ops.pop(), a, b))
    prev = None
    for t in tokenize(s):
        if isinstance(t, int):
            nums.append(t)
        elif t == "(":
            ops.append(t)
        elif t == ")":
            while ops[-1] != "(":
                reduce()
            ops.pop()
        else:
            if t == "-" and prev in (None, "("):
                nums.append(0)      # 一元负号：0 - x
            while ops and ops[-1] != "(" \
                    and PREC[ops[-1]] >= PREC[t]:
                reduce()            # 同级左结合
            ops.append(t)
        prev = t
    while ops:
        reduce()
    return nums[0]
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 弹栈条件写成 `>`：`"8-3-2"` 得 `7`，`"8/4/2"` 得 `4`，应为 `3` 和 `1`。
- 除法直接 `//`：`"(-7)/2"` 得 `-4`，应为 `-3`；`int(a / b)` 在 `10^17` 以上丢精度。
- 一元负号不补 `0`：`"-(2+3)"` 和 `"(-1)+2"` 都会 `IndexError`。
- 不校验：`"1 2"` 静默返回 `1`，`"2*-3"`、`"()"`、`"1+"` 抛 `IndexError`。

**追问。**
- 加 `^`（右结合）、小数、变量？：换优先级表；右结合的弹出条件改成 `>`，结构不变。
- 为什么用迭代而不是递归下降？：括号嵌套 `10^5` 层也不会爆栈。

**同模式。** LC 227 基本计算器 II、LC 224 基本计算器、LC 772 基本计算器 III、LC 150 逆波兰表达式求值
