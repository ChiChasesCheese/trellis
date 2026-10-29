---
id: tlc-evaluate-reverse-polish-notation-2-code
node: a.evaluate-reverse-polish-notation
type: qa
step: 2
---
## Q
**LC 150 逆波兰表达式求值**｜写出 Python 实现

计算后缀表达式 `tokens`（长度至多 `10^4`，元素是 `+ - * /` 或 `[-200, 200]` 内的整数）的值；除法向零截断，输入合法，中间结果在 32 位范围内。

## A
**思路。** 栈存还没用掉的操作数。数字入栈；运算符弹出两个数，先弹的是右操作数 `b`、后弹的是左操作数 `a`，把 `a op b` 压回。除法单独写成向零截断。

```python
from operator import add, mul, sub


def _div(a: int, b: int) -> int:
    q = abs(a) // abs(b)                   # 先对绝对值做整除，再补符号：结果向零截断
    return q if (a < 0) == (b < 0) else -q


def eval_rpn(tokens: list[str]) -> int:
    ops = {"+": add, "-": sub, "*": mul, "/": _div}
    stack: list[int] = []
    for tok in tokens:
        if tok in ops:
            b = stack.pop()                # 先弹出的是右操作数
            a = stack.pop()
            stack.append(ops[tok](a, b))
        else:
            stack.append(int(tok))         # "-11" 不在 ops 里，会走到这里
    return stack[0]
```

运行：`["2","1","+","3","*"]` → `9`，`["4","13","5","/","+"]` → `6`，`["10","6","9","3","+","-11","*","/","*","17","+","5","+"]` → `22`，`["-7","2","/"]` → `-3`，`["5"]` → `5`。

**复杂度。** 时间 `O(n)`，每个 token 处理一次；空间 `O(n)`，最坏所有数字先于运算符入栈。

**写法要点。** `operator` 模块的 `add / sub / mul` 放进字典做分派，替代一串 `if/elif`；判断「是不是运算符」而不是「是不是数字」，负数 `"-11"` 自然走到 `int(tok)`；整数除法自己写成「绝对值整除再补符号」，全程整数运算，不依赖浮点。
