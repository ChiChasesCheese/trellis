---
id: lct-learn-data-structures-3-4
node: data-structures.3.4
type: qa
step: 1
---
## Q
**常用数据结构 › 栈 › 合法括号字符串（RBS）**｜学习卡

套路是什么？

## A
**一句话。** 括号串合法当且仅当每个前缀里 `(` 不少于 `)` 且最后相等；只要数量就用一个计数器，要知道谁和谁配对、在哪里就用栈（多种括号栈存字符，要位置栈存下标）。

下图：按题目要的信息选工具。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<polygon points="78.0,22.0 87.0,9.5 253.0,9.5 262.0,22.0 253.0,34.5 87.0,34.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="26.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只要数量？（合法吗、补几个）</text>
<rect x="18.1" y="90.0" width="103.8" height="70" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="70" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">计数器 bal</text>
<text x="70" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">( 加一，) 减一</text>
<text x="70" y="136.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">前缀 bal ≥ 0</text>
<text x="70" y="151.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">结尾 bal = 0</text>
<polygon points="189.0,80.0 198.0,67.5 292.0,67.5 301.0,80.0 292.0,92.5 198.0,92.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要知道配对位置？</text>
<rect x="139.0" y="140.0" width="101.9" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">栈存字符</text>
<text x="190" y="171.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">) 来了弹栈比对</text>
<rect x="246.6" y="140.0" width="96.9" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="295" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">栈存下标</text>
<text x="295" y="171.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">栈底放哨兵 -1</text>
<path d="M 78.0 22.0 L 70.0 22.0 L 70.0 90.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="70.0,90.0 67.0,83.7 73.0,83.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="58" y="45" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 262.0 22.0 L 310.0 22.0 L 310.0 50.0 L 245.0 50.0 L 245.0 67.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="245.0,67.5 242.0,61.2 248.0,61.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="322" y="40" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 245.0 92.5 L 245.0 112.0 L 190.0 112.0 L 190.0 140.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="190.0,140.0 187.0,133.7 193.0,133.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否：多种括号</text>
<path d="M 245.0 92.5 L 245.0 112.0 L 295.0 112.0 L 295.0 140.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="295.0,140.0 292.0,133.7 298.0,133.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="305" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是：长度</text>
</svg>

```python
def is_valid(s):                     # LC 20：三种括号
    pair = {')': '(', ']': '[', '}': '{'}
    st = []
    for ch in s:
        if ch not in pair:
            st.append(ch)            # 左括号入栈
        elif not st or st.pop() != pair[ch]:   # 先判空，再比配对
            return False
    return not st                    # 还有未配对的左括号：非法

def min_add(s):                      # LC 921：只要数量，用计数器
    add = bal = 0                    # add：缺的 (，bal：待配对的 (
    for ch in s:
        if ch == '(':
            bal += 1
        elif bal:
            bal -= 1                 # 配对
        else:
            add += 1                 # 多余的 )：前面补一个 (
    return add + bal                 # 剩下的 ( 各补一个 )
```

**要点。**
- 为什么对？：每个 `)` 与左边最近的未配对 `(` 配对，`bal >= 0` 保证它存在，配对不交叉，所以配对关系唯一确定；只有一种括号时栈里全是 `(`，一个整数 `bal` 就够。
- LC 1249、LC 1190 怎么改？：1249 栈存下标，标记多余的 `)` 和扫完剩下的 `(`，最后统一删；1190 先用栈预处理配对 `pair[i]`，再沿字符串走，遇括号跳到配对处并掉头，不用真的反转。
- LC 856 怎么改？：深度计数，每个 `()` 贡献 `2^深度`，并列相加。
- LC 678 怎么改？：`*` 让未配对数变成区间 `[lo, hi]`，`lo` 按 `*` 当 `)`、`hi` 按 `*` 当 `(` 更新，`hi < 0` 失败，`lo` 截回 `0`，最后 `lo == 0`。

**易错点。**
- LC 20 先弹栈再判空：`"]"` 栈空时 `pop` 抛错；`"([)]"` 应得 `False`，`"("` 应得 `False`（要检查栈空）。
- LC 921：`")("` 应得 `2`，多余的 `)` 与剩下的 `(` 都要补。
- LC 678 不把 `lo` 截回 `0`：`"(*)("` 应得 `False`，不截断会误判为 `True`。

**对应题目。** LC 921 使括号有效的最少添加、LC 1249 移除无效的括号、LC 1190 反转每对括号间的子串、LC 856 括号的分数、LC 20 有效的括号、LC 678 有效的括号字符串
