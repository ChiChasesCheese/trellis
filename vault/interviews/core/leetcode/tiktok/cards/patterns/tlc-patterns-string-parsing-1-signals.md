---
id: tlc-patterns-string-parsing-1-signals
node: patterns.string-parsing
type: qa
step: 1
---
## Q
**字符串处理与表达式解析｜信号**

什么样的题面该想到"用栈解析字符串"？计算器、解码字符串、括号配对各是什么信号？KMP 和滚动哈希在什么时候才需要？

## A
**用栈解析的信号：**
- 表达式里有**优先级**（`*` `/` 高于 `+` `-`）或**括号**：计算器 LC 224、227、772；这些题的标准解较长，先用同属「栈求值」的逆波兰表达式把操作数栈的用法练熟（例：LC 150 逆波兰表达式求值；高频：LC 227 基本计算器 II、LC 224 基本计算器）。
- 有**嵌套结构**，里层先于外层处理：`3[a2[c]]` 解码 LC 394、括号的分数 LC 856（例：LC 394 字符串解码）。
- 需要"**撤销最近一步**"或匹配最近的一个：路径 `..` 返回上一级 LC 71，相邻重复项消除 LC 1209，括号配对 LC 20、1249（例：LC 71 简化路径；高频：LC 20 有效的括号）。
- 输入长度 `10^5` 到 `3 * 10^5`（LC 227、224 是 `3 * 10^5`）：必须一次扫描 `O(n)`，不能反复切片（例：LC 1249 移除无效的括号）。

**两种处理方式：**
- **栈**：遇到"开始一个子结构"就保存现场（压栈），"结束"时恢复并合并（弹栈）。
- **递归下降**：每遇到 `(` 递归解析括号内部，返回值当作一个数；逻辑清晰，但深度等于括号嵌套层数。

**其他字符串信号：**
- 按分隔符拆开再逐段比较：版本号，`split(".")` 后转成整数，缺失当 0（例：LC 165 比较版本号）。
- 逐位运算的大数（加法、乘法）：LC 415，模拟竖式（例：LC 43 字符串相乘）。

**KMP / 滚动哈希什么时候才用**：在长文本里反复找模式串（子串匹配），`s.find(t)` 的朴素最坏 `O(nm)`；要保证线性才手写 KMP，或用滚动哈希（Rabin-Karp）比较窗口。LC 题里一般 `in` / `find` 就够，除非明确要求实现。长度固定的窗口比较，直接把窗口放进集合就行（例：LC 187 重复的DNA序列）。

**近似信号：**
- 只有括号、没有优先级 ⇒ 不需要栈，一个计数器就够；有 `+`、`-` 和括号时用"符号 + 结果栈"（LC 224）（例：LC 921 使括号有效的最少添加）。
- 全是比较 / 计数 ⇒ 哈希表，不是栈（例：LC 49 字母异位词分组）。

**例题：** LC 150 逆波兰表达式求值

给字符串数组 `tokens`，它是一个逆波兰表示法（后缀表达式，reverse Polish notation：运算符写在两个操作数之后）的算术表达式，求它的整数值。运算符只有 `+ - * /`；整数除法**向零截断**；不会除以零；输入一定合法；答案和所有中间结果都在 32 位整数范围内。`1 <= tokens.length <= 10^4`，`tokens[i]` 是运算符或 `[-200, 200]` 内的整数。

```python
from operator import add, mul, sub
def _div(a: int, b: int) -> int:
    q = abs(a) // abs(b)                   # 先对绝对值做整除，再补符号：结果向零截断
    return q if (a < 0) == (b < 0) else -q
def eval_rpn(tokens: list[str]) -> int:
    ops = {"+": add, "-": sub, "*": mul, "/": _div}
    stack: list[int] = []
    for tok in tokens:
        if tok in ops:
            b = stack.pop()                # 先弹出的是右操作数
            a = stack.pop()
            stack.append(ops[tok](a, b))
        else:
            stack.append(int(tok))         # "-11" 不在 ops 里，会走到这里
    return stack[0]
```

**例题：** LC 394 字符串解码

给一个编码后的字符串 `s`，返回解码后的字符串。编码规则 `k[encoded_string]` 表示方括号内部的 `encoded_string` 正好重复 `k` 次，`k` 为正整数。输入总是有效的，没有额外空格，方括号总是合法的；原始数据不含数字，数字只表示重复次数（不会出现 `3a` 或 `2[4]`）；测试用例保证输出长度不超过 `10^5`。`1 <= s.length <= 30`，`s` 由小写英文字母、数字和方括号 `[]` 组成，`s` 中所有整数的取值范围为 `[1, 300]`。

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

给一个 Unix 风格的绝对路径 `path`（以 `'/'` 开头），把它化成规范路径。规则：`'.'` 表示当前目录；`'..'` 表示上一级目录（根目录没有上一级，留在根目录）；多个连续的 `'/'` 视为一个；其他形式的点（如 `'...'`、`'....'`）是合法的目录名。规范路径必须以 `'/'` 开头，两个目录名之间只有一个 `'/'`，末尾不能有 `'/'`（根目录除外），且不含 `'.'` 或 `'..'`。`1 <= path.length <= 3000`，`path` 由英文字母、数字、`'.'`、`'/'`、`'_'` 组成，且是有效的绝对路径。

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

给由 `'('`、`')'` 和小写字母组成的字符串 `s`。删除**最少**数目的 `'('` 或 `')'`（可以删任意位置的括号），使剩下的括号字符串有效，返回任意一个合法结果。有效字符串指：空串或只含小写字母的串；可以写成 `AB`（`A`、`B` 都有效）；可以写成 `(A)`（`A` 有效）。`1 <= s.length <= 10^5`，`s[i]` 是 `'('`、`')'` 或小写英文字母。

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

**例题：** LC 165 比较版本号

给两个版本号字符串 `version1` 和 `version2`，比较它们。版本号由被点 `'.'` 分开的修订号组成，修订号的值是它转换为整数并忽略前导零的结果。比较时按从左到右的顺序依次比较修订号；如果其中一个版本号的修订号较少，缺失的修订号视为 `0`。`version1 < version2` 返回 `-1`，`version1 > version2` 返回 `1`，否则返回 `0`。`1 <= version1.length, version2.length <= 500`，只包含数字和 `'.'`，都是有效版本号，所有修订号都可以存储在 32 位整数中。

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

**例题：** LC 43 字符串相乘

给定两个以字符串形式表示的非负整数 `num1` 和 `num2`，返回它们的乘积，乘积也表示为字符串。不能使用任何内置的 BigInteger 库，也不能直接把输入转换为整数。`1 <= num1.length, num2.length <= 200`，`num1` 和 `num2` 只由数字组成，且都不含前导零（除了数字 `0` 本身）。

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

**例题：** LC 187 重复的DNA序列

DNA 序列由字符 `'A'`、`'C'`、`'G'`、`'T'` 组成。给字符串 `s`，返回所有在 `s` 中出现**不止一次**的、长度为 `10` 的子串，顺序任意（每个只返回一次）。`0 <= s.length <= 10^5`，`s[i]` 是 `A`、`C`、`G`、`T` 之一。

```python
from collections import Counter
def find_repeated_dna_sequences(s: str) -> list[str]:
    L = 10
    code = {"A": 0, "C": 1, "G": 2, "T": 3}     # 每个碱基 2 位
    mask = (1 << 2 * L) - 1                      # 只保留最近 10 个碱基的 20 位
    count: Counter[int] = Counter()
    res: list[str] = []
    window = 0
    for i, ch in enumerate(s):
        window = ((window << 2) | code[ch]) & mask   # 左移挤掉最老的碱基，低位放新碱基
        if i >= L - 1:                               # 窗口满 10 个才开始计数
            count[window] += 1
            if count[window] == 2:                   # 恰好第二次出现时收集，避免重复
                res.append(s[i - L + 1 : i + 1])
    return res
```

**例题：** LC 921 使括号有效的最少添加

括号字符串有效，当且仅当：它是空串；或可写成 `AB`（`A`、`B` 都有效）；或可写成 `(A)`（`A` 有效）。给定只含 `'('` 和 `')'` 的字符串 `s`，每次操作可以在**任意位置**插入一个括号。返回使 `s` 有效所需的**最少插入次数**。`1 <= s.length <= 1000`。

```python
def min_add_to_make_valid(s: str) -> int:
    open_cnt = add = 0                        # open_cnt：还没配对的 '('；add：必须补的 '('
    for ch in s:
        if ch == "(":
            open_cnt += 1
        elif open_cnt:                        # 有 '(' 可配
            open_cnt -= 1
        else:                                 # ')' 前面没有 '(' 可配：补一个 '('
            add += 1
    return add + open_cnt                     # 剩下没配上的 '(' 各需补一个 ')'
```

**例题：** LC 49 字母异位词分组

给一个字符串数组 `strs`，把**字母异位词**（anagram，字母相同、顺序不同的词）分到同一组，按任意顺序返回。`1 <= strs.length <= 10^4`，`0 <= strs[i].length <= 100`，`strs[i]` 只含小写字母。

```python
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    for s in strs:
        count = [0] * 26                       # 26 个字母的出现次数就是指纹
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)         # list 不可哈希，转成 tuple 才能当键
    return list(groups.values())
```

**例题：** LC 227 基本计算器 II

计算只含非负整数、`+ - * /` 和空格的表达式，整数除法向 `0` 取整，不能用 `eval`；`1 <= s.length <= 3 * 10^5`。

```python
def calculate(s: str) -> int:
    stack: list[int] = []
    num, op = 0, "+"
    for ch in s + "+":
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
            stack.append(int(stack.pop() / num))
        op, num = ch, 0
    return sum(stack)
```

**例题：** LC 224 基本计算器

计算含非负整数、`+`、`-`、括号和空格的表达式（`-` 可作一元运算），不能用 `eval`；`1 <= s.length <= 3 * 10^5`。

```python
def calculate(s: str) -> int:
    stack: list[tuple[int, int]] = []
    res, num, sign = 0, 0, 1
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch in "+-":
            res += sign * num
            num, sign = 0, 1 if ch == "+" else -1
        elif ch == "(":
            stack.append((res, sign))
            res, sign = 0, 1
        elif ch == ")":
            res += sign * num
            num = 0
            prev_res, prev_sign = stack.pop()
            res = prev_res + prev_sign * res
    return res + sign * num
```

**例题：** LC 20 有效的括号

只含 `()[]{}` 的字符串 `s`，判断括号是否按类型和顺序正确闭合；`1 <= s.length <= 10^4`。

```python
def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
```
