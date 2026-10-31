---
id: tlc-core-basic-calculator-ii
node: p2.basic-calculator-ii
type: qa
---
## Q
**LC 227 基本计算器 II**｜Medium · LC TikTok 近 3 个月热度 70/100（全时段 66） · CodeTop 国内累计 20 次 · 最近 2025-11-23（国内 CodeTop） · 也在：Amazon

给字符串表达式 `s`，实现一个基本计算器计算并返回它的值。整数除法仅保留整数部分（向 0 取整）。表达式总是有效的，所有中间结果在 `[-2^31, 2^31 - 1]` 内；不允许使用 `eval()` 这类把字符串当数学表达式计算的内置函数。`1 <= s.length <= 3 * 10^5`，`s` 由整数和算符 `+ - * /` 组成，中间由一些空格隔开；所有整数是非负整数，范围 `[0, 2^31 - 1]`；答案保证是 32 位整数。例：`"3+2*2"` → `7`；`" 3/2 "` → `1`；`" 3+5 / 2 "` → `5`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用一个栈存「待相加的项」：`+` / `-` 把带符号的数压栈，`*` / `/` 当场和栈顶合并；最后把栈里所有项相加。末尾补一个 `"+"` 当哨兵，逼出最后一个数。`O(n)`。

**识别。** 「四则运算 + 优先级」：乘除先于加减。没有括号，所以不需要两个栈，只要把加减留到最后、乘除立刻算掉。`n` 到 `3×10^5` → 一遍扫描 `O(n)`，且不能递归。

**推导。** 暴力：先扫一遍把所有乘除算掉、替换成结果，再扫一遍算加减，两轮；或者把表达式转成后缀表达式（逆波兰）再求值 → 浪费：题目没有括号，不需要完整的调度场算法 → 记住上一个运算符，读完一个数才结算它；加减项各自独立，最后求和。

**简单解法。** 先切成记号（token），第一遍把 `*` `/` 算掉，第二遍只剩 `+` `-`，从左到右求和。

```python
import re


def calculate(s: str) -> int:
    tokens = re.findall(r"\d+|[-+*/]", s)          # 空格自然被丢掉；数字和算符交替出现
    flat: list[int | str] = [int(tokens[0])]
    for i in range(1, len(tokens), 2):
        op, nxt = tokens[i], int(tokens[i + 1])
        if op == "*":
            flat[-1] *= nxt                         # 乘除立刻并进前一个数
        elif op == "/":
            flat[-1] = int(flat[-1] / nxt)          # 向 0 取整；// 向下取整，遇负数会错
        else:
            flat += [op, nxt]                       # 加减留到第二遍
    total = flat[0]
    for i in range(1, len(flat), 2):                # 第二遍：只剩 + -，从左到右
        total += flat[i + 1] if flat[i] == "+" else -flat[i + 1]
    return total
```

时间 `O(n)`，空间 `O(n)`；比主解多一份记号列表，思路上是「先乘除后加减」的字面翻译，不依赖栈。

最优解：

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

运行：`"3+2*2"` → `7`，`" 3/2 "` → `1`，`" 3+5 / 2 "` → `5`，`"3-5/2"` → `1`，`"14-3/2"` → `13`，`"42"` → `42`，`"0"` → `0`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（栈最坏存 `n/2` 个项）。

**拓展优化。**
- 不用栈，`O(1)` 空间：只留已结算的 `total` 和还没定的最后一项 `last`，乘除改 `last`，加减才把 `last` 并进 `total`：
```python
def calculate_o1(s: str) -> int:
    total = last = num = 0
    op = "+"                                        # op 是 num 左边的运算符
    for ch in s + "+":                              # 末尾补 "+" 当哨兵，结算最后一个数
        if ch == " ":
            continue
        if ch.isdigit():
            num = num * 10 + int(ch)
            continue
        if op == "+":
            total += last                           # 上一项定下来了
            last = num
        elif op == "-":
            total += last
            last = -num
        elif op == "*":
            last *= num                             # 乘除只改还没定的 last
        else:
            last = int(last / num)                  # 向 0 取整
        op, num = ch, 0
    return total + last
```

**易错点。**
- 除法向 0 取整：`"3-5/2"` 里栈顶是 `-5`，用 `//` 得 `-3`，结果 `0`；用 `int(a / b)` 得 `-2`，结果 `1`（正确）。
- 最后一个数需要哨兵触发结算：不补 `"+"` 时，`"42"` 返回 `0`，`"3+2*2"` 返回 `5`。
- 空格要跳过，且多位数要累加：`num = num * 10 + int(ch)`。

**追问。**
- 加括号（LC 224 / LC 772）：用两个栈（数字栈、运算符栈）按优先级归约，遇 `)` 归约到 `(`；`"2*(5+5*2)/3+(6/2+8)"` → `21`。
- 加入一元负号或指数 `^`：一元负号当作 `0 - x`，`^` 右结合、优先级最高。

**同模式。** LC 224 基本计算器、LC 772 基本计算器 III、LC 150 逆波兰表达式求值、LC 394 字符串解码。
