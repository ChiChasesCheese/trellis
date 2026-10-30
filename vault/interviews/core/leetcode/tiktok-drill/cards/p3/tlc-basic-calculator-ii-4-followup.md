---
id: tlc-basic-calculator-ii-4-followup
node: p3.basic-calculator-ii
type: qa
step: 4
---
## Q
**LC 227 基本计算器 II**｜追问

面试官接着问：（1）表达式里加上括号（LC 772 的做法）？（2）能不能把栈省掉，只用 `O(1)` 额外空间？（3）如果输入不保证有效，应该检查什么？

## A
1. **加括号**：用两个栈（数字栈、运算符栈），按优先级归约。遇到运算符，先把栈顶优先级不低于它的运算符归约掉再入栈；遇到 `)` 一直归约到 `(`。`"2*(5+5*2)/3+(6/2+8)"` → `21`。
```python
def calculate_paren(s: str) -> int:
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    nums: list[int] = []
    ops: list[str] = []

    def apply() -> None:
        b, a, op = nums.pop(), nums.pop(), ops.pop()
        if op == "+":
            nums.append(a + b)
        elif op == "-":
            nums.append(a - b)
        elif op == "*":
            nums.append(a * b)
        else:
            nums.append(int(a / b))

    i = 0
    while i < len(s):
        ch = s[i]
        if ch.isdigit():
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            nums.append(int(s[i:j]))
            i = j
            continue
        if ch == "(":
            ops.append(ch)
        elif ch == ")":
            while ops[-1] != "(":
                apply()
            ops.pop()
        elif ch in prec:
            while ops and ops[-1] != "(" and prec[ops[-1]] >= prec[ch]:
                apply()
            ops.append(ch)
        i += 1
    while ops:
        apply()
    return nums[0]
```
2. **`O(1)` 空间**：栈里真正会被修改的只有栈顶。保留两个数：`total`（已确定的和）和 `last`（当前项）。遇到 `*` / `/` 就改 `last`；遇到 `+` / `-` 就把 `last` 并进 `total`，再让 `last = ±num`。
3. **非法输入**：连续运算符、除以 0、以运算符开头或结尾、括号不匹配、数字溢出。题目保证有效，面试里先说明假设，再说明哪些检查会加在循环里。

**Python 提醒**：`int(a / b)` 用浮点除法，结果超过 `2^53` 时会失去精度，题目的中间值在 32 位范围内所以安全；换成 `a // b` 要处理符号。`str.isdigit()` 对 Unicode 数字（如 `"²"`）也返回 `True`，而 `int("²")` 会抛 `ValueError`，输入不可信时改用 `"0" <= ch <= "9"`。
