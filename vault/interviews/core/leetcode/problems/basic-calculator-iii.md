---
slug: basic-calculator-iii
---
## Q
**LC 772 基本计算器 III**｜Hard

计算含非负整数、`+ - * /` 和括号的表达式（整数除法向零截断），不许用 `eval`。

## A
**一句话。** 拆成「加法项」之和：`*` `/` 立刻并入上一项，遇到 `(` 把外层压栈开新层，遇到 `)` 求和后当一个数交还。

```python
def trunc_div(a, b):
    q = abs(a) // abs(b)          # 向零截断
    return q if (a < 0) == (b < 0) else -q

def calculate(s):
    saved = []                    # 括号外层 (terms, op)
    terms = []                    # 当前层的加法项
    op, num = "+", 0

    def apply():                  # 把 num 按 op 并入当前层
        if op == "+":
            terms.append(num)
        elif op == "-":
            terms.append(-num)
        elif op == "*":
            terms[-1] *= num
        else:
            terms[-1] = trunc_div(terms[-1], num)

    for ch in s + "+":            # 补 "+" 冲刷最后一个数
        if "0" <= ch <= "9":
            num = num * 10 + int(ch)
        elif ch == "(":
            saved.append((terms, op))
            terms, op, num = [], "+", 0
        else:                     # + - * / )
            apply()
            if ch == ")":
                value = sum(terms)
                terms, op = saved.pop()
                num = value       # 括号结果当作一个数
            else:
                op, num = ch, 0
    return sum(terms)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 除法直接用 `//`：`(0-3)/2` 应得 `-1`，`//` 得 `-2`。
- 忘了冲刷最后一个数：`6-4/2` 得 `2`，应为 `4`，所以补一个 `"+"`。
- 括号结果丢了括号前的运算符：`6-(1+2)` 应得 `3`，当成加项得 `9`。

**追问。**
- 加一元负号和空格（LC 224）？：开头或 `(` 后的 `-` 当作 `0-`，空格直接跳过。
- 加右结合的幂运算 `^`？：升级成递归下降或调度场（shunting-yard），为每个运算符定义优先级。

**同模式。** LC 224 基本计算器、LC 227 基本计算器 II、LC 150 逆波兰表达式求值、LC 394 字符串解码
