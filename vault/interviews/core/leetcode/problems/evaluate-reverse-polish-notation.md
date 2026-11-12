---
slug: evaluate-reverse-polish-notation
---
## Q
**LC 150 逆波兰表达式求值**｜Medium

给后缀表达式 `tokens`（运算符 `+ - * /`，整数除法向零截断），求它的值。

## A
**一句话。** 一个栈：数字入栈，遇到运算符弹出两个数（先弹的是右操作数），算完压回。

```python
def eval_rpn(tokens):
    ops = {"+": lambda a, b: a + b,
           "-": lambda a, b: a - b,
           "*": lambda a, b: a * b,
           # 绝对值整除再补符号，才是向零截断
           "/": lambda a, b: abs(a) // abs(b)
                * (1 if (a < 0) == (b < 0) else -1)}
    stack = []
    for tok in tokens:
        if tok in ops:
            b = stack.pop()     # 先弹出的是右操作数
            a = stack.pop()
            stack.append(ops[tok](a, b))
        else:
            stack.append(int(tok))  # "-11" 也走这里
    return stack[0]
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用 `a // b`：向下取整，`-7 // 2 == -4`，题目要 `-3`。
- 弹出顺序写反成 `op(b, a)`：`["4","13","5","/","+"]` 算成 `4 + 5/13 = 4`，应为 `6`。
- 用 `tok.isdigit()` 判数字：`"-11"` 不是纯数字，被当成运算符；改判运算符。

**追问。**
- 给的是中缀表达式（LC 224）？：调度场算法按优先级转后缀，或用数栈加运算符栈边扫边算。
- 怎么构造表达式树？：栈里放节点，运算符弹出两个子节点组成新节点，最后栈顶是根。

**同模式。** LC 224 基本计算器、LC 227 基本计算器 II、LC 20 有效的括号、LC 394 字符串解码
