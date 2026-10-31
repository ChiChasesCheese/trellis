---
id: tlc-basic-calculator-ii-2-code
node: p2.basic-calculator-ii
type: qa
step: 2
---
## Q
**LC 227 基本计算器 II**｜写出 Python 实现

字符串 `s`（长度 `1` 到 `3×10^5`）是由非负整数、`+ - * /` 和空格组成的有效表达式，整数除法向 0 取整，中间结果和答案都在 32 位整数范围内。不使用 `eval()`，返回表达式的值。

## A
**思路。** 栈里存待相加的项。扫描时记住数字左边的运算符 `op`：读完一个数后按 `op` 结算——`+` 压 `num`，`-` 压 `-num`，`*` 与栈顶相乘，`/` 与栈顶相除（向 0 取整）。字符串末尾补 `"+"`，让最后一个数也被结算。

```python
def calculate(s: str) -> int:
    stack: list[int] = []                 # 栈里是待相加的项；* / 当场并进栈顶
    num, op = 0, "+"                      # op 是 num 左边的运算符
    for ch in s + "+":                    # 末尾补一个 "+" 当哨兵，逼出最后一个数
        if ch == " ":
            continue
        if ch.isdigit():
            num = num * 10 + int(ch)
            continue
        if op == "+":
            stack.append(num)
        elif op == "-":
            stack.append(-num)
        elif op == "*":
            stack.append(stack.pop() * num)
        else:
            stack.append(int(stack.pop() / num))      # 向 0 取整；// 向下取整，遇负数会错
        op, num = ch, 0
    return sum(stack)
```

运行：`"3+2*2"` → `7`，`" 3/2 "` → `1`，`" 3+5 / 2 "` → `5`，`"3-5/2"` → `1`，`"14-3/2"` → `13`，`"42"` → `42`，`"2147483647"` → `2147483647`。

**复杂度。** 时间 `O(n)`：每个字符处理一次；空间 `O(n)`：栈里最多 `n/2` 项。

**写法要点。** `s + "+"` 的哨兵让循环体不需要在末尾再写一次结算；`continue` 提前处理空格和数字，主体只剩「遇到运算符」一种情况；`int(a / b)` 向 0 取整，在值不超过 `2^31` 时浮点除法精确到足以得到正确的整数部分——若要完全避免浮点，写成 `a // b if a * b >= 0 else -(-a // b)`；`sum(stack)` 一次求和，减法已经在压栈时变成了负数。
