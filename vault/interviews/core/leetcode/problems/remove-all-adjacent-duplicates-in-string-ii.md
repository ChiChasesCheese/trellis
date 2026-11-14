---
slug: remove-all-adjacent-duplicates-in-string-ii
---
## Q
**LC 1209 删除字符串中的所有相邻重复项 II**｜Medium

反复删除字符串中 `k` 个相邻且相等的字母（删后两侧接拢），直到不能删，返回结果。

## A
**一句话。** 栈存 `(字符, 连续次数)`，与栈顶相同就计数加一，达到 `k` 整项弹出。

**图解。** 栈里每项是「字符·连续次数」，次数凑够 `k` 就整项弹出，两侧自动接拢。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 310 214">
<text x="10" y="14" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读到</text>
<text x="122" y="14" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">栈：字符·次数（k = 3）</text>
<text x="10" y="39" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">deee</text>
<rect x="122" y="22" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="142" y="38" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">d·1</text>
<text x="214" y="39" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">e·3 弹出</text>
<text x="10" y="70" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">deeedbb</text>
<rect x="122" y="53" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="142" y="69" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">d·2</text>
<rect x="164" y="53" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="184" y="69" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">b·2</text>
<text x="10" y="101" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">deeedbbccc</text>
<rect x="122" y="84" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="142" y="100" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">d·2</text>
<rect x="164" y="84" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="184" y="100" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">b·2</text>
<text x="214" y="101" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">c·3 弹出</text>
<text x="10" y="132" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">deeedbbcccb</text>
<rect x="122" y="115" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="142" y="131" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">d·2</text>
<text x="214" y="132" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">b·3 弹出</text>
<text x="10" y="163" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">deeedbbcccbd</text>
<text x="126" y="163" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">空</text>
<text x="214" y="163" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d·3 弹出</text>
<text x="10" y="194" text-anchor="start" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">deeedbbcccbdaa</text>
<rect x="122" y="177" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="142" y="193" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">a·2</text>
<text x="214" y="194" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">结果 aa</text>
</svg>

```python
def remove_duplicates(s, k):
    stack = []                       # (字符, 连续次数)
    for ch in s:
        if stack and stack[-1][0] == ch:
            _, cnt = stack.pop()
            if cnt + 1 < k:          # 凑够 k 就不放回
                stack.append((ch, cnt + 1))
        else:
            stack.append((ch, 1))
    return "".join(ch * cnt for ch, cnt in stack)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 一遍 `groupby` 每段保留 `len % k` 个：删后相邻段会合并成新的重复，`("deeedbbcccbdaa", 3)` 得 `'ddbbbdaa'`，应为 `'aa'`。
- 拼接时不乘计数：`("aaab", 4)` 得 `'ab'`，应为 `'aaab'`。

**追问。**
- 想省栈空间？：在 `list(s)` 上原地覆盖，写指针加计数数组，达到 `k` 时写指针回退 `k - 1` 位。

**同模式。** LC 1047 删除字符串中的所有相邻重复项、LC 2390 从字符串中移除星号、LC 735 小行星碰撞、LC 71 简化路径
