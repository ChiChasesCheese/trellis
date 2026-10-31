---
id: tlc-reverse-substrings-between-each-pair-of-parentheses-0-whole
node: c.reverse-substrings-between-each-pair-of-parentheses
type: qa
---
## Q
**LC 1190 反转每对括号间的子串**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 1 次 · 最近 2021-07-15（国内 CodeTop）

给定只含小写字母和括号的字符串 `s`。按从括号内到外的顺序，逐层反转每对匹配括号中的字符串，返回最终结果，结果中不应包含任何括号。`1 <= s.length <= 2000`，括号保证成对出现。例：`"(abcd)"` → `"dcba"`；`"(u(love)i)"` → `"iloveu"`（先反转 `love`，再反转整个）；`"(ed(et(oc))el)"` → `"leetcode"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 预先配好每对括号，然后只扫一遍：遇到括号就「瞬移」到配对的括号并掉头，不用真的反转任何子串。

**识别。** 「括号嵌套 + 反转」：栈配对括号是基础。进一步发现，反转的嵌套本质是行进方向的翻转，可以用「碰到括号跳到配对位置并反向」一次线性扫描完成。

**推导。** 直接模拟：栈顶维护当前层的字符，遇到 `)` 弹出栈顶层、反转后接到上一层，反转嵌套 `d` 层的字符被复制 `d` 次，最坏 `O(n²)`。洞察：每个字符只会在一条固定的路径上被读到——往右读，碰到 `(` 就跳到配对的 `)` 然后向左读；碰到 `)` 就跳到配对的 `(` 然后向右读。每次跳转翻转方向。配对表一遍栈预处理，之后每个字符恰好读一次。

**简单解法。** 栈里每一层存一个字符列表，遇到 `)` 就把顶层反转后接回上一层。

```python
def reverse_parentheses_stack(s: str) -> str:
    stack: list[list[str]] = [[]]                # 每层括号一个字符列表
    for ch in s:
        if ch == "(":
            stack.append([])                     # 进入新的一层
        elif ch == ")":
            inner = stack.pop()
            stack[-1].extend(reversed(inner))    # 这一层结束：反转后接到上一层
        else:
            stack[-1].append(ch)
    return "".join(stack[0])
```

`n <= 2000`，最坏 `O(n²)` 次字符复制，完全够用；括号层数很深、字符串很长时才需要 `O(n)` 的方案。

最优解：

```python
def reverse_parentheses(s: str) -> str:
    n = len(s)
    pair = [0] * n                               # 括号位置 -> 配对括号位置
    stack: list[int] = []
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            j = stack.pop()
            pair[i], pair[j] = j, i
    res: list[str] = []
    i, step = 0, 1                               # step 为 +1 向右读，-1 向左读
    while i < n:
        if s[i] in "()":
            i = pair[i]                          # 跳到配对括号
            step = -step                         # 并掉头
        else:
            res.append(s[i])
        i += step                                # 越过括号继续读
    return "".join(res)
```

运行：`"(abcd)"` → `"dcba"`，`"(u(love)i)"` → `"iloveu"`，`"(ed(et(oc))el)"` → `"leetcode"`；`"a(bc)d"` → `"acbd"`，`"abc"` → `"abc"`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**拓展优化。**
- 栈方案的 `O(n²)` 来自深层嵌套里的字符被反复复制；瞬移法每个字符只读一次，括号只跳转。

**易错点。**
- 跳转后忘了 `i += step`：停在括号上又跳回去，死循环。
- 掉头方向没有取反而是写死：嵌套两层的反转会还原方向，必须 `step = -step`。
- 栈方案里接回上一层时忘了 `reversed`：`"(abcd)"` 会输出 `"abcd"`。

**追问。**
- 保留括号：只在输出时保留括号字符，但方向逻辑不变。
- 括号可以不匹配：需要先判断合法性，用同一个栈。

**同模式。** LC 20 有效的括号、LC 394 字符串解码、LC 726 原子的数量、LC 856 括号的分数、LC 1249 移除无效的括号。
