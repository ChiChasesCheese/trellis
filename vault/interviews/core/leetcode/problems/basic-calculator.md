---
slug: basic-calculator
---
## Q
**LC 224 基本计算器**｜Hard

计算只含数字、`+`、`-`、括号和空格的表达式字符串的值（`-` 可作一元），不许用 `eval`。

## A
**一句话。** 一遍扫描，栈保存括号前的 `(res, sign)`，遇 `)` 把括号结果乘上括号前的符号并回外层。

```python
def calculate(s):
    st = []
    res, num, sign = 0, 0, 1
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch in "+-":
            res += sign * num       # 结算上一个数
            num, sign = 0, 1 if ch == "+" else -1
        elif ch == "(":
            st.append((res, sign))  # 括号内从 0 重算
            res, sign = 0, 1
        elif ch == ")":
            res += sign * num
            num = 0
            pres, psign = st.pop()
            res = pres + psign * res
    return res + sign * num
```

**复杂度。** 时间 `O(n)`，空间 `O(括号深度)`。

**易错点。**
- 括号结果漏乘括号前的符号：`"1-(2+3)"` 得 `6`，应为 `-4`。
- 最后一个数忘了在循环外结算：`"1+2"` 得 `1`。
- 一元负号不必特判：开头或 `(` 后 `num` 仍是 `0`，`"-(2+3)"` 自然得 `-5`。

**追问。**
- 加入乘除（LC 772）怎么办？：需要优先级，用数字栈加运算符栈，优先级不低于当前的先归约。
- 不用栈能做吗？：递归下降，遇 `(` 递归，遇 `)` 返回。

**同模式。** LC 227 基本计算器 II、LC 772 基本计算器 III、LC 394 字符串解码、LC 726 原子的数量
