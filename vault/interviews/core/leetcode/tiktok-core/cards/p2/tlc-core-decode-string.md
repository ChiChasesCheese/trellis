---
id: tlc-core-decode-string
node: p2.decode-string
type: qa
---
## Q
**LC 394 字符串解码**｜Medium · LC TikTok 近 3 个月热度 81/100（全时段 75） · 近一年被问：美国 0 次、国内 1 次 · CodeTop 国内累计 58 次 · 最近 2026-08-20（国内 CodeTop） · 也在：Amazon、LeetCode Hot 100

给一个编码后的字符串 `s`，返回解码后的字符串。编码规则 `k[encoded_string]` 表示方括号内部的 `encoded_string` 正好重复 `k` 次，`k` 为正整数。输入总是有效的，没有额外空格，方括号总是合法的；原始数据不含数字，数字只表示重复次数（不会出现 `3a` 或 `2[4]`）；测试用例保证输出长度不超过 `10^5`。`1 <= s.length <= 30`，`s` 由小写英文字母、数字和方括号 `[]` 组成，`s` 中所有整数的取值范围为 `[1, 300]`。例：`"3[a]2[bc]"` → `"aaabcbc"`；`"3[a2[c]]"` → `"accaccacc"`；`"2[abc]3[cd]ef"` → `"abcabccdcdcdef"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用栈保存「外层的状态」：读到 `[` 就把「已拼好的前缀」和「重复次数」压栈并清空当前层；读到 `]` 就弹栈，把当前层重复 `times` 次接在前缀后面。一遍扫描，`O(输出长度)`。

**识别。** 「括号嵌套 + 先里后外」是栈或递归的信号：最内层先展开，结果再交给外层使用，后进先出。`k` 可能有多位数（范围到 300），要累加解析。

**推导。** 暴力：反复用正则替换最内层的 `k[...]`，直到没有括号——每一轮都要重新扫描整个字符串 → 浪费：嵌套越深重复扫描越多 → 括号配对的顺序就是栈的出入顺序。

**简单解法。** 正则反复替换：每轮只匹配方括号里没有方括号的最内层 `k[abc]` 并展开，直到没有 `[`。

```python
import re

def decode_string(s: str) -> str:
    inner = re.compile(r"(\d+)\[([a-z]*)\]")       # 方括号里只有字母 = 最内层
    while "[" in s:
        s = inner.sub(lambda m: m.group(2) * int(m.group(1)), s)   # 一轮展开所有最内层
    return s
```

时间 `O(嵌套深度 * 串长)`、空间 `O(输出长度)`；`s.length <= 30` 足够，但每轮都重扫整串，嵌套深、输出长时慢，栈只扫一遍。

最优解：

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

运行：`"3[a]2[bc]"` → `"aaabcbc"`，`"3[a2[c]]"` → `"accaccacc"`，`"2[abc]3[cd]ef"` → `"abcabccdcdcdef"`，`"abc3[cd]xyz"` → `"abccdcdcdxyz"`，`"10[a]"` → `"aaaaaaaaaa"`，`"a"` → `"a"`。

**复杂度。** 时间 `O(输出长度)`（嵌套里的重复串被复制多次，总复制量与最终输出同量级）；空间 `O(嵌套深度 + 输出长度)`。

**拓展优化。**
- 递归下降（recursive descent）：`parse(i)` 解析到 `]` 或末尾，深度等于嵌套层数，`s.length <= 30` 不会爆栈。

```python
def decode_string(s: str) -> str:
    def parse(i: int) -> tuple[str, int]:
        out: list[str] = []
        while i < len(s) and s[i] != "]":          # 遇到 ] 说明这一层结束，交还给调用者
            if s[i].isdigit():
                j = i
                while s[j].isdigit():
                    j += 1
                times = int(s[i:j])                # 多位数的重复次数
                inner, i = parse(j + 1)            # 跳过 [，递归解内层；i 停在对应的 ]
                out.append(inner * times)
                i += 1                             # 跳过 ]
            else:
                out.append(s[i])
                i += 1
        return "".join(out), i

    return parse(0)[0]
```

- 只要解码后的长度：栈里存整数长度，拼接换成乘加，不分配内存；`"300[300[300[a]]]"` 的长度是 `27000000`。

```python
def decoded_length(s: str) -> int:
    stack: list[tuple[int, int]] = []              # (进入 [ 之前的长度, 这一层的重复次数)
    cur, num = 0, 0                                # cur：当前层已解码的长度
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)               # 多位数的次数
        elif ch == "[":
            stack.append((cur, num))               # 保存外层现场，进入内层从 0 开始数
            cur, num = 0, 0
        elif ch == "]":
            prev, times = stack.pop()
            cur = prev + cur * times               # 字符串拼接换成长度的乘加
        else:
            cur += 1                               # 一个普通字母贡献长度 1
    return cur
```

**易错点。**
- 次数是多位数：用 `num = num * 10 + int(ch)`。写成 `num = int(ch)` 时，`"10[a]"` 得到空串 `""`，正确是 `"aaaaaaaaaa"`。
- 前缀必须压栈：只压次数、丢掉前缀时，`"ab2[c]"` 得到 `"cc"`，正确是 `"abcc"`。
- 进入 `[` 后要把 `num` 清零：否则 `"3[a]2[bc]"` 里的 `2` 会接在上一个 `3` 后面变成 `32`，输出长度 `67` 而不是 `7`。

**追问。**
- 要第 `k` 个字符（LC 880）：从后往前反推，不展开字符串。

**同模式。** LC 224 基本计算器、LC 227 基本计算器 II、LC 726 原子的数量、LC 20 有效的括号。
