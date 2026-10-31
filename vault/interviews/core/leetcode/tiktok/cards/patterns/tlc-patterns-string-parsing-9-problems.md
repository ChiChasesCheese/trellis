---
id: tlc-patterns-string-parsing-9-problems
node: patterns.string-parsing
type: qa
step: 9
---
## Q
**字符串处理与表达式解析｜本组用到解析与字符串栈的题**

按变形分类，这个题组里哪些题属于字符串解析？

## A
**计算器**
- LC 227 基本计算器 II
- LC 224 基本计算器
- 计算器梯度题：先校验再求值（高频）

**嵌套结构**
- LC 394 字符串解码
- LC 385 迷你语法分析器（高频）

**分段比较 / 路径**
- LC 71 简化路径
- LC 151 反转字符串中的单词（高频）
- LC 1360 日期之间隔几天（高频）

**括号 / 相邻重复的栈**
- LC 20 有效的括号
- LC 301 删除无效的括号（回溯或 BFS）
- LC 921 使括号有效的最少添加（高频）
- LC 678 有效的括号字符串（高频）
- LC 32 最长有效括号（高频）

**逐位模拟**
- LC 415 字符串相加
- LC 43 字符串相乘
- LC 68 文本左右对齐（按行贪心填充 + 空格分配）

**相邻：字符串算法**

提示：看到"优先级 / 括号 / 嵌套"想栈；先写出栈里放什么（项、符号、字符串加次数、下标），再写遇到每种字符时的动作。

**例题：** LC 227 基本计算器 II

计算只含非负整数、`+ - * /` 和空格的表达式（整数除法向 `0` 取整），不能用 `eval`。`1 <= s.length <= 3 * 10^5`，结果在 32 位整数内。

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

**例题：** LC 224 基本计算器

计算含非负整数、`+`、`-`、括号和空格的表达式，`-` 可以作一元运算，不能用 `eval`。`1 <= s.length <= 3 * 10^5`。

```python
def calculate(s: str) -> int:
    stack: list[tuple[int, int]] = []     # 进括号前保存 (已累计的结果, 括号前的符号)
    res, num, sign = 0, 0, 1
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch in "+-":
            res += sign * num             # 结算上一个数
            num, sign = 0, 1 if ch == "+" else -1
        elif ch == "(":
            stack.append((res, sign))     # 括号内从 0 重新算
            res, sign = 0, 1
        elif ch == ")":
            res += sign * num             # 结算括号里最后一个数
            num = 0
            prev_res, prev_sign = stack.pop()
            res = prev_res + prev_sign * res   # 括号结果乘上括号前的符号，再并回去
    return res + sign * num
```

**例题：** LC 394 字符串解码

解码 `k[encoded]`（方括号内的串重复 `k` 次，可嵌套）。`1 <= s.length <= 30`，`k` 在 `[1, 300]`，输入总是有效。

```python
def decode_string(s: str) -> str:
    stack: list[tuple[str, int]] = []     # (进入 [ 之前已拼好的前缀, 这一层的重复次数)
    cur, num = "", 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)      # 次数可能是多位数
        elif ch == "[":
            stack.append((cur, num))
            cur, num = "", 0              # 进入新的一层，从空串重新拼
        elif ch == "]":
            prev, times = stack.pop()
            cur = prev + cur * times      # 把这一层重复 times 次接到前缀后面
        else:
            cur += ch
    return cur
```

**例题：** LC 71 简化路径

把 Unix 风格绝对路径化简成规范路径（`.` 是当前目录，`..` 是上一级，连续 `/` 合并，`...` 是普通目录名）。`1 <= path.length <= 3000`。

```python
def simplify_path(path: str) -> str:
    stack: list[str] = []
    for part in path.split('/'):       # '//' 切出空串，'.' 与空串都只是噪声
        if part == '..':
            if stack:                  # 根目录没有上一级：栈空时忽略
                stack.pop()
        elif part and part != '.':     # '...' 之类是合法名字，照常入栈
            stack.append(part)
    return '/' + '/'.join(stack)
```

**例题：** LC 20 有效的括号

判断只含 `()[]{}` 的字符串 `s` 的括号是否有效（类型匹配、顺序正确）。`1 <= s.length <= 10^4`。

```python
def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}     # 右括号 -> 它该配的左括号
    stack: list[str] = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:   # 栈空，或栈顶类型对不上
                return False
        else:
            stack.append(ch)
    return not stack                            # 还有没闭合的左括号就是无效
```

**例题：** LC 301 删除无效的括号

字符串 `s` 含小写字母和括号，删除最少数量的括号使其有效，返回所有可能的结果（去重）。`1 <= s.length <= 25`，括号至多 `20` 个。

```python
def remove_invalid_parentheses(s: str) -> list[str]:
    left_rem = right_rem = 0                   # 至少还要删多少个 ( 和 )
    for ch in s:
        if ch == "(":
            left_rem += 1
        elif ch == ")":
            if left_rem:
                left_rem -= 1                  # 这个 ) 能和前面某个 ( 配对
            else:
                right_rem += 1                 # 前面没有可配的 (，这个 ) 必须删
    delta = {"(": 1, ")": -1}
    res: set[str] = set()                      # 不同位置删同样的括号会得到同一个串，用集合去重
    path: list[str] = []
    def dfs(i: int, left: int, right: int, balance: int) -> None:
        if left < 0 or right < 0 or balance < 0 or left + right > len(s) - i:
            return                             # 删多了、) 已无法挽回、或剩下的字符不够删
        if i == len(s):
            if left == right == balance == 0:
                res.add("".join(path))
            return
        ch = s[i]
        if ch == "(":
            dfs(i + 1, left - 1, right, balance)       # 删掉这个 (
        elif ch == ")":
            dfs(i + 1, left, right - 1, balance)       # 删掉这个 )
        path.append(ch)                                # 保留这个字符
        dfs(i + 1, left, right, balance + delta.get(ch, 0))
        path.pop()
    dfs(0, left_rem, right_rem, 0)
    return list(res)
```

**例题：** LC 415 字符串相加

两个以字符串表示的非负整数 `num1`、`num2`，返回它们的和（字符串），不能转成整数或用大整数库。长度 `1..10^4`，无前导零。

```python
from itertools import zip_longest
def add_strings(num1: str, num2: str) -> str:
    digits: list[str] = []
    carry = 0
    # 从个位开始配对；短的那个用 "0" 补齐
    for a, b in zip_longest(reversed(num1), reversed(num2), fillvalue="0"):
        carry, d = divmod(int(a) + int(b) + carry, 10)    # 一步同时得到进位和当前位
        digits.append(str(d))
    if carry:
        digits.append("1")
    return "".join(reversed(digits))
```

**例题：** LC 43 字符串相乘

两个以字符串表示的非负整数 `num1`、`num2`，返回它们的乘积（字符串），不能转成整数或用大整数库。长度 `1..200`，无前导零。

```python
def multiply(num1: str, num2: str) -> str:
    a = [int(c) for c in reversed(num1)]  # 个位在下标 0
    b = [int(c) for c in reversed(num2)]
    res = [0] * (len(a) + len(b))         # a[i] * b[j] 落在第 i + j 位
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            res[i + j] += x * y           # 先只累加，不进位
    carry = 0
    for k in range(len(res)):             # 统一进一遍位
        carry, res[k] = divmod(res[k] + carry, 10)
    while len(res) > 1 and res[-1] == 0:  # 去掉高位多余的 0；乘积为 0 时保留一个 "0"
        res.pop()
    return "".join(map(str, reversed(res)))
```

**例题：** LC 68 文本左右对齐

把单词排成每行恰好 `maxWidth` 个字符的两端对齐文本：每行贪心放尽量多的单词，空格尽量均分且左侧多；最后一行与单词独占的行左对齐。`1 <= words.length <= 300`，`1 <= maxWidth <= 100`。

```python
def full_justify(words: list[str], max_width: int) -> list[str]:
    lines: list[str] = []
    i, n = 0, len(words)
    while i < n:
        j, used = i + 1, len(words[i])             # words[i:j] 是当前行，used 是单词总长加最少空格
        while j < n and used + 1 + len(words[j]) <= max_width:
            used += 1 + len(words[j])              # 贪心：能放就放，每个新词多占 1 个空格 + 词长
            j += 1
        line = words[i:j]
        if j == n or len(line) == 1:               # 最后一行或只有一个词：左对齐，右侧补空格
            lines.append(" ".join(line).ljust(max_width))
        else:
            gaps = len(line) - 1
            spaces = max_width - sum(map(len, line))
            q, r = divmod(spaces, gaps)            # 每个缝至少 q 个空格，前 r 个缝再多 1 个
            parts = [w + " " * (q + (k < r)) for k, w in enumerate(line[:-1])]
            lines.append("".join(parts) + line[-1])
        i = j
    return lines
```

**例题：** 计算器梯度题（先校验再求值）

给一个字符串表达式 `s`，实现整数计算器 `calculate(s)`。面试官逐级加条件：（1）只有 `+ - * /` 和空格，没有括号，要处理优先级，除法是整数除法（向零取整）；（2）再加括号和一元负号；（3）先校验表达式是否合法（空串、非法字符、括号不配对、连续运算符、缺操作数），合法才计算。`1 <= len(s) <= 3 * 10^5`，操作数是非负整数；一元负号只出现在表达式开头或 `(` 之后；除数不会是 `0`。

```python
import re
PREC = {"+": 1, "-": 1, "*": 2, "/": 2}
TOKEN = re.compile(r"\s*(?:(\d+)|(\S))")
def tokenize(s: str) -> list[int | str]:
    """数字变成 int，其余单字符原样保留；遇到非法字符抛 ValueError。"""
    tokens: list[int | str] = []
    for m in TOKEN.finditer(s):
        num, ch = m.groups()
        if num is not None:
            tokens.append(int(num))
        elif ch in "+-*/()":
            tokens.append(ch)
        else:
            raise ValueError(f"illegal character {ch!r}")
    return tokens
def is_valid(s: str) -> bool:
    """先校验：空串、非法字符、括号不配对、连续运算符、缺操作数都返回 False。
    一元负号只允许出现在表达式开头或 '(' 之后。"""
    try:
        tokens = tokenize(s)
    except ValueError:
        return False
    depth, want_operand, prev = 0, True, None
    for tok in tokens:
        if want_operand:
            if isinstance(tok, int):
                want_operand = False
            elif tok == "(":
                depth += 1
            elif tok == "-" and prev in (None, "("):
                pass
            else:
                return False
        else:
            if tok == ")":
                depth -= 1
                if depth < 0:
                    return False
            elif tok in PREC:
                want_operand = True
            else:
                return False
        prev = tok
    return bool(tokens) and not want_operand and depth == 0
def _apply(op: str, a: int, b: int) -> int:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q
def calculate(s: str) -> int:
    if not is_valid(s):
        raise ValueError("invalid expression")
    nums: list[int] = []
    ops: list[str] = []
    def reduce_top() -> None:
        b, a = nums.pop(), nums.pop()
        nums.append(_apply(ops.pop(), a, b))
    prev = None
    for tok in tokenize(s):
        if isinstance(tok, int):
            nums.append(tok)
        elif tok == "(":
            ops.append(tok)
        elif tok == ")":
            while ops[-1] != "(":
                reduce_top()
            ops.pop()
        else:
            if tok == "-" and prev in (None, "("):
                nums.append(0)
            while ops and ops[-1] != "(" and PREC[ops[-1]] >= PREC[tok]:
                reduce_top()
            ops.append(tok)
        prev = tok
    while ops:
        reduce_top()
    return nums[0]
```

**例题：** LC 385 迷你语法分析器

给一个字符串 `s`，表示整数的嵌套列表，实现解析器返回对应的 `NestedInteger`。列表里的每个元素只可能是整数，或整数的嵌套列表。`NestedInteger` 接口：`NestedInteger()` 创建空列表，`NestedInteger(v)` 创建单个整数，`add(x)` 把 `x` 追加进列表。`1 <= s.length <= 5 * 10^4`，`s` 只含数字、方括号、负号 `-`、逗号，保证可解析，所有数值在 `[-10^6, 10^6]`。

```python
import re
def deserialize(s: str) -> NestedInteger:
    tokens = iter(re.findall(r"\[|\]|-?\d+", s))
    def parse(tok: str) -> NestedInteger:
        if tok != "[":
            return NestedInteger(int(tok))
        lst = NestedInteger()
        for nxt in tokens:
            if nxt == "]":
                break
            lst.add(parse(nxt))
        return lst
    return parse(next(tokens))
```

**例题：** LC 151 反转字符串中的单词

给字符串 `s`，反转其中单词的顺序。单词是由非空格字符组成的串，`s` 里用至少一个空格分隔单词，开头、结尾、单词之间都可能有多余的空格。返回单词顺序颠倒、单词之间只用**一个**空格连接、没有前导或尾随空格的字符串。`1 <= s.length <= 10^4`，`s` 只含英文字母、数字和空格，至少有一个单词。

```python
def reverse_words(s: str) -> str:
    words: list[str] = []
    i = len(s) - 1
    while i >= 0:
        if s[i] == " ":
            i -= 1
            continue
        end = i + 1
        while i >= 0 and s[i] != " ":
            i -= 1
        words.append(s[i + 1:end])
    return " ".join(words)
```

**例题：** LC 1360 日期之间隔几天

编写程序计算两个日期之间隔了多少天。日期以字符串 `YYYY-MM-DD` 给出，保证是 `1971` 年到 `2100` 年之间的有效日期。

```python
MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
def days_between_dates(date1: str, date2: str) -> int:
    def is_leap(y: int) -> bool:
        return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)
    def to_days(s: str) -> int:
        y, m, d = map(int, s.split("-"))
        days = sum(365 + is_leap(k) for k in range(1971, y))
        days += sum(MONTH_DAYS[:m - 1]) + (m > 2 and is_leap(y))
        return days + d
    return abs(to_days(date1) - to_days(date2))
```

**例题：** LC 921 使括号有效的最少添加

括号字符串有效，当且仅当：它是空串；或可写成 `AB`（`A`、`B` 都有效）；或可写成 `(A)`（`A` 有效）。给定只含 `'('` 和 `')'` 的字符串 `s`，每次操作可以在**任意位置**插入一个括号。返回使 `s` 有效所需的**最少插入次数**。`1 <= s.length <= 1000`。

```python
def min_add_to_make_valid(s: str) -> int:
    open_cnt = add = 0
    for ch in s:
        if ch == "(":
            open_cnt += 1
        elif open_cnt:
            open_cnt -= 1
        else:
            add += 1
    return add + open_cnt
```

**例题：** LC 678 有效的括号字符串

给一个只含 `'('`、`')'` 和 `'*'` 三种字符的字符串 `s`，判断它是否有效。有效的条件：每个 `'('` 都有对应的 `')'`，每个 `')'` 都有对应的 `'('`，`'('` 必须在对应的 `')'` 之前；`'*'` 可以当作单个 `')'`、单个 `'('` 或空串。`1 <= s.length <= 100`，`s[i]` 只能是 `'('`、`')'`、`'*'`。

```python
def check_valid_string(s: str) -> bool:
    lo = hi = 0
    for ch in s:
        lo += 1 if ch == '(' else -1
        hi += 1 if ch != ')' else -1
        if hi < 0:
            return False
        lo = max(lo, 0)
    return lo == 0
```

**例题：** LC 32 最长有效括号

给一个只包含 `'('` 和 `')'` 的字符串 `s`，找出最长的有效（格式正确且连续）括号子串的长度。「有效」指每个左括号都有对应的右括号将其闭合，比如 `"(()())"`。`0 <= s.length <= 3 * 10^4`，`s[i]` 为 `'('` 或 `')'`。

```python
def longest_valid_parentheses(s: str) -> int:
    stack = [-1]
    best = 0
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if stack:
                best = max(best, i - stack[-1])
            else:
                stack.append(i)
    return best
```
