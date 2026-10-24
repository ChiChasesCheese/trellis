---
id: tlc-tt-basic-calculator-ladder-5-alt
node: a.tt-basic-calculator-ladder
type: qa
step: 5
---
## Q
**计算器梯度题（先校验再求值）**｜另一种解法

梯度的第一级只有 `+ - * /` 和空格，没有括号，除法向零取整，操作数是非负整数。有没有比「双栈」更短的写法？它在哪一级失效？

## A
**一个栈存「项」，最后求和。** 把表达式看成若干项（term）相加：乘除立刻并入上一项，加减把新项压栈（减号压负数），最后 `sum(stack)`。用「上一个运算符」`sign` 延迟处理，字符串末尾补一个哨兵运算符把最后一个数结算掉。

```python
def calculate_no_parens(s: str) -> int:
    """阶梯第一级：只有 + - * /，没有括号。栈里存每一项（term）的值，最后求和。"""
    stack: list[int] = []
    num, sign = 0, "+"                       # sign 是 num 前面的那个运算符
    for ch in s + "+":                       # 末尾补一个哨兵运算符，把最后一个数结算掉
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch != " ":
            if sign == "+":
                stack.append(num)
            elif sign == "-":
                stack.append(-num)
            elif sign == "*":
                stack.append(stack.pop() * num)
            else:                            # 除法向零取整：负数先取反再除
                top = stack.pop()
                stack.append(top // num if top >= 0 else -(-top // num))
            sign, num = ch, 0
    return sum(stack)
```

`"3+2*2"` → `7`，`" 3/2 "` → `1`，`" 3+5 / 2 "` → `5`，`"14-3/2"` → `13`，`"2*3-4/3*2"` → `4`。时间 `O(n)`，空间 `O(n)`（最坏每项一个数）。

**怎么选。**
- 只有第一级（LC 227）：这版更短，十行，面试里先写它。
- 有括号：一个「项栈」不够，因为括号内的整体要作为一个操作数参与外层的乘除；需要双栈，或者遇到 `(` 时递归求子表达式（递归深度受括号嵌套限制）。
- 需要先校验、嵌套很深或要扩展运算符：用双栈版本，结构统一，改优先级表即可。
