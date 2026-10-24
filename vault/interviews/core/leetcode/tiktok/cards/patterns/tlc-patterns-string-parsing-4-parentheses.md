---
id: tlc-patterns-string-parsing-4-parentheses
node: patterns.string-parsing
type: qa
step: 4
---
## Q
**字符串处理与表达式解析｜带括号：只有加减（LC 224）与加减乘除（LC 772）**

遇到括号怎样"保存现场、算完括号再合并"？有乘除时怎样递归处理？

## A
**LC 224（只有加减和括号）**：遇到 `(` 把"之前的结果和括号前的符号"压栈，括号内从 0 重新算；遇到 `)` 弹栈，括号结果乘以括号前的符号并入。

```python
def calculate_i(s: str) -> int:
    result, sign, num = 0, 1, 0
    stack: list[tuple[int, int]] = []      # 进入括号前保存 (之前的结果, 括号前的符号)
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch in "+-":
            result += sign * num
            num, sign = 0, 1 if ch == "+" else -1
        elif ch == "(":
            stack.append((result, sign))
            result, sign = 0, 1
        elif ch == ")":
            result += sign * num
            prev_result, prev_sign = stack.pop()
            result = prev_result + prev_sign * result
            num = 0
    return result + sign * num
print(calculate_i("(1+(4+5+2)-3)+(6+8)"), calculate_i("-(2+3)"), calculate_i("2-(5-6)"))   # 23 -5 3
```

时间 `O(n)`，空间为括号嵌套深度。

**LC 772（四则运算加括号）**：递归下降：`parse()` 解析到匹配的 `)` 或末尾，内部就是 LC 227 的栈算法；遇到 `(` 就调用 `parse()`，返回值当成一个数。

```python
def calculate_iii(s: str) -> int:
    s, i = s.replace(" ", ""), 0
    def parse() -> int:
        nonlocal i
        stack: list[int] = []
        num, op = 0, "+"
        while i < len(s):
            ch = s[i]
            i += 1
            if ch.isdigit():
                num = num * 10 + int(ch)
            if ch == "(":
                num = parse()              # 括号里的整体当作一个数
            if ch in "+-*/)" or i == len(s):
                if op == "+":
                    stack.append(num)
                elif op == "-":
                    stack.append(-num)
                elif op == "*":
                    stack.append(stack.pop() * num)
                else:
                    stack.append(int(stack.pop() / num))   # 向零截断；中间结果在 32 位内，浮点除法足够精确
                op, num = ch, 0
                if ch == ")":
                    break
        return sum(stack)
    return parse()
print(calculate_iii("6-4/2"), calculate_iii("2*(5+5*2)/3+(6/2+8)"))   # 4 21
```
