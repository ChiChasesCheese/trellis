---
id: tlc-patterns-string-parsing-2-template
node: patterns.string-parsing
type: qa
step: 2
---
## Q
**字符串处理与表达式解析｜模板：处理优先级的计算器（LC 227）**

只有 `+ - * /` 的表达式，怎样一遍扫描、用一个栈处理优先级？

## A
关键思路：**把表达式看作若干"项"的和**。`+`、`-` 只是给下一项带上符号并入栈；`*`、`/` 立即和栈顶的项结合。最后把栈里所有项相加。

```python
def div0(a: int, b: int) -> int:
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q      # 向零截断

def calculate_ii(s: str) -> int:
    stack: list[int] = []                  # 乘除立即算，加减的项先入栈，最后求和
    num = 0
    op = "+"                               # 上一个运算符，作用于刚读完的 num
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)
        if (not ch.isdigit() and ch != " ") or i == len(s) - 1:
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            else:
                stack.append(div0(stack.pop(), num))
            op, num = ch, 0
    return sum(stack)
```

运行：`"3+2*2"` → `7`；`" 3/2 "` → `1`；`" 3+5 / 2 "` → `5`；`"1-7/2"` → `-2`；`"42"` → `42`。时间 `O(n)`，空间 `O(n)`。

- **延迟一步处理**：`op` 保存的是**上一个**运算符；当读到下一个运算符（或到达末尾）时，才把刚读完的 `num` 与 `op` 结合。所以第一项的 `op` 初值是 `"+"`。
- 减法转成加负数 `stack.append(-num)`，这样后面的 `*`、`/` 作用在带符号的项上，优先级自然正确。
- 空格直接跳过（不更新 `op`、不清空 `num`）；末尾字符是数字或空格时 `i == len(s) - 1` 保证最后一项被处理。
- 可以把栈换成两个变量（`last_term` 与 `total`）做到 `O(1)` 空间。
- 除法截断方向：题目说"仅保留整数部分"，即**向零截断**（`-7/2 = -3`），Python 的 `//` 是向下取整（`-7//2 = -4`），要自己处理。
