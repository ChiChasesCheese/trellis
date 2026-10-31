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
- LC 772 基本计算器 III

**嵌套结构**
- LC 394 字符串解码
- LC 856 括号的分数

**分段比较 / 路径**
- LC 165 比较版本号
- LC 71 简化路径

**括号 / 相邻重复的栈**
- LC 1249 移除无效的括号
- LC 1209 删除字符串中的所有相邻重复项 II
- LC 20 有效的括号
- LC 301 删除无效的括号（回溯或 BFS）

**逐位模拟**
- LC 415 字符串相加
- LC 43 字符串相乘
- LC 68 文本左右对齐（按行贪心填充 + 空格分配）

**相邻：字符串算法**
- LC 3474 字典序最小的生成字符串（字符串匹配）
- LC 2468 根据限制分割消息（枚举分段数）

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

**例题：** LC 772 基本计算器 III

计算含非负整数、`+ - * /` 和括号的表达式（整数除法向零截断），不能用 `eval`。`1 <= s.length <= 10^4`，表达式有效。

```python
def trunc_div(a: int, b: int) -> int:
    q = abs(a) // abs(b)               # 先按绝对值整除，再补符号：向零截断
    return q if (a < 0) == (b < 0) else -q
def calculate(s: str) -> int:
    saved: list[tuple[list[int], str]] = []   # 进入括号前的 (外层各项, 括号前的运算符)
    terms: list[int] = []              # 当前层的加法项：加减号只负责决定项的符号
    op, num = "+", 0                   # num 前面等待结合的运算符；正在读的数
    def apply() -> None:               # 把 num 按 op 并入当前层
        if op == "+":
            terms.append(num)
        elif op == "-":
            terms.append(-num)
        elif op == "*":
            terms[-1] *= num           # 乘除立刻与上一项结合
        else:
            terms[-1] = trunc_div(terms[-1], num)
    for ch in s + "+":                 # 末尾补一个 "+"，把最后一个数冲刷进去
        if "0" <= ch <= "9":
            num = num * 10 + int(ch)
        elif ch == "(":
            saved.append((terms, op))  # 暂存外层，开一层新的
            terms, op, num = [], "+", 0
        else:                          # + - * / )
            apply()
            if ch == ")":
                value = sum(terms)     # 括号内算完，它就是外层的一个“数”
                terms, op = saved.pop()
                num = value
            else:
                op, num = ch, 0
    return sum(terms)
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

**例题：** LC 856 括号的分数

平衡括号串 `S` 的分数：`()` 得 `1`，`AB` 得 `A + B`，`(A)` 得 `2 * A`。`2 <= S.length <= 50`。

```python
def score_of_parentheses(s: str) -> int:
    stack = [0]                             # stack[-1] 是当前这一层已累计的分数
    for ch in s:
        if ch == "(":
            stack.append(0)                 # 开新的一层
        else:
            inner = stack.pop()
            stack[-1] += max(2 * inner, 1)  # "()" 内部为 0，记 1；否则翻倍
    return stack[0]
```

**例题：** LC 165 比较版本号

比较两个以 `.` 分隔修订号的版本号，缺失的修订号视为 `0`，返回 `-1`、`0` 或 `1`。每个字符串长度 `1..500`，修订号在 32 位整数内。

```python
from itertools import zip_longest
def compare_version(version1: str, version2: str) -> int:
    # 按 "." 切开；短的一边用 "0" 补齐，"1.0" 和 "1.0.0.0" 就自然相等
    for a, b in zip_longest(version1.split("."), version2.split("."), fillvalue="0"):
        x, y = int(a), int(b)           # int() 同时去掉前导零
        if x != y:
            return -1 if x < y else 1
    return 0
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

**例题：** LC 1249 移除无效的括号

字符串 `s` 含小写字母和括号，删去最少的括号使其有效，返回任意一个结果。`1 <= s.length <= 10^5`。

```python
def min_remove_to_make_valid(s: str) -> str:
    drop: set[int] = set()                 # 要删掉的括号下标
    opens: list[int] = []                  # 还没配对的 "(" 的下标
    for i, ch in enumerate(s):
        if ch == "(":
            opens.append(i)
        elif ch == ")":
            if opens:
                opens.pop()                # 配上最近的 "("
            else:
                drop.add(i)                # 前面没有可配的 "("：这个 ")" 多余
    drop.update(opens)                     # 扫完仍没配上的 "(" 也多余
    return "".join(ch for i, ch in enumerate(s) if i not in drop)
```

**例题：** LC 1209 删除字符串中的所有相邻重复项 II

反复删除 `k` 个相邻且相等的字母（两侧拼接后继续），返回最终字符串。`1 <= s.length <= 10^5`，`2 <= k <= 10^4`，只含小写字母。

```python
def remove_duplicates(s: str, k: int) -> str:
    stack: list[tuple[str, int]] = []      # (字符, 当前连续出现次数)
    for ch in s:
        if stack and stack[-1][0] == ch:
            _, cnt = stack.pop()
            if cnt + 1 < k:                # 还没凑够 k 个：把计数加一放回去；凑够就不放回，整段被删
                stack.append((ch, cnt + 1))
        else:
            stack.append((ch, 1))
    return "".join(ch * cnt for ch, cnt in stack)
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

**例题：** LC 3474 字典序最小的生成字符串

`str1`（长 `n`，由 `T`/`F` 组成）和 `str2`（长 `m`）。长 `n + m - 1` 的 `word` 满足：`str1[i] == 'T'` 时 `word[i..i+m-1] == str2`，为 `'F'` 时不相等。返回字典序最小的 `word`，不存在返回 `""`。`1 <= n <= 10^4`，`1 <= m <= 500`。

```python
def generate_string(str1: str, str2: str) -> str:
    n, m = len(str1), len(str2)
    word: list[str | None] = [None] * (n + m - 1)      # None 表示这一位还没有被 'T' 钉死
    for i, flag in enumerate(str1):
        if flag != "T":
            continue
        for j, ch in enumerate(str2):                  # 把 str2 铺到 [i, i+m)
            if word[i + j] not in (None, ch):          # 两个 'T' 窗口在重叠处要求不同字母：无解
                return ""
            word[i + j] = ch
    forced = [ch is not None for ch in word]           # 被 'T' 钉死的位置不能再动
    res = [ch or "a" for ch in word]                   # 自由位先填最小字母 'a'
    for i, flag in enumerate(str1):
        if flag == "F" and res[i : i + m] == list(str2):   # 'F' 窗口不小心等于 str2：必须改一位
            for j in range(i + m - 1, i - 1, -1):          # 改窗口里最靠右的自由位，对字典序伤害最小
                if not forced[j]:
                    res[j] = "b"
                    break
            else:
                return ""                                  # 窗口里全是被钉死的位：无解
    return "".join(res)
```

**例题：** LC 2468 根据限制分割消息

把 `message` 切成若干段，每段末尾加后缀 `<a/b>`（`a` 是编号，`b` 是总段数）；除最后一段外每段长度恰为 `limit`，去掉后缀拼回必须还原 `message`，且段数尽量少。返回切分结果，不可能则返回空数组。`1 <= message.length <= 10^4`，`1 <= limit <= 10^4`。

```python
def split_message(message: str, limit: int) -> list[str]:
    n = len(message)
    total_parts = 0
    index_digits = 0                       # 编号 1..b 的位数总和
    for b in range(1, n + 1):              # 每段至少装 1 个字符，所以 b <= n
        index_digits += len(str(b))
        suffix = 3 + len(str(b))           # "<", "/", ">" 加上总段数 b 的位数
        capacity = b * (limit - suffix) - index_digits    # b 段一共能装的字符数
        if limit - suffix - len(str(b)) <= 0:             # 连最后一段（编号位数最多）都装不下 1 个字符
            return []
        if capacity >= n:
            total_parts = b
            break
    else:
        return []
    out: list[str] = []
    pos = 0
    for a in range(1, total_parts + 1):
        tail = f"<{a}/{total_parts}>"
        take = limit - len(tail)           # 除最后一段外都刚好填满 limit
        out.append(message[pos:pos + take] + tail)
        pos += take
    return out
```
