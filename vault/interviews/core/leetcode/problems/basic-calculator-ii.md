---
slug: basic-calculator-ii
---
## Q
**LC 227 基本计算器 II**｜Medium

计算只含非负整数、`+ - * /` 和空格的表达式，除法向 0 取整，不许用 `eval`。

## A
**一句话。** 栈存待相加的项：`+` / `-` 压入带符号的数，`*` / `/` 当场与栈顶合并，最后求和。

```python
def calculate(s):
    stack = []
    num, op = 0, "+"          # op 是 num 左边的运算符
    for ch in s + "+":        # 末尾哨兵逼出最后一个数
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
            stack.append(int(stack.pop() / num))  # 向 0 取整
        op, num = ch, 0
    return sum(stack)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 除法用 `//`：`"3-5/2"` 栈顶 `-5 // 2 = -3`，结果 `0`，应为 `1`。
- 不补末尾哨兵：最后一个数没人结算，`"42"` 返回 `0`。
- 多位数只取一位：要 `num = num * 10 + int(ch)`，并跳过空格。

**追问。**
- 加括号（LC 224 / 772）？：数字栈加运算符栈按优先级归约，遇 `)` 归约到 `(`。

**同模式。** LC 224 基本计算器、LC 772 基本计算器 III、LC 150 逆波兰表达式求值、LC 394 字符串解码
