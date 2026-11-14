---
slug: remove-all-occurrences-of-a-substring
---
## Q
**LC 1910 删除一个字符串中所有出现的给定子字符串**｜Medium

反复删除 `s` 中最左边出现的 `part`，直到不再出现，返回剩下的字符串。

## A
**一句话。** 用栈逐字符压入，栈顶一旦拼出 `part` 就整段弹掉，删除后新接上的部分自然会被继续检查。

**图解。** 每次栈顶拼出 `part` 就整段弹掉，后面的字符接着和栈里剩下的拼。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 150">
<text x="10" y="14" text-anchor="start" font-size="10" font-family="ui-monospace,Menlo,monospace" style="fill:var(--dim,#6b7280)">s = daabcbaabcbc，part = abc</text>
<rect x="20" y="26" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="32.0" y="42.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">d</text>
<rect x="44" y="26" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56.0" y="42.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">a</text>
<rect x="68" y="26" width="24" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="42.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">a</text>
<rect x="92" y="26" width="24" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="104.0" y="42.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">b</text>
<rect x="116" y="26" width="24" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="128.0" y="42.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">c</text>
<text x="200" y="42" text-anchor="start" font-size="12" font-family="ui-monospace,Menlo,monospace" style="fill:var(--accent,#3b6fd4)">→ da</text>
<rect x="20" y="62" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="32.0" y="78.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">d</text>
<rect x="44" y="62" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56.0" y="78.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">a</text>
<rect x="68" y="62" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="78.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">b</text>
<rect x="92" y="62" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="104.0" y="78.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">a</text>
<rect x="116" y="62" width="24" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="128.0" y="78.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">a</text>
<rect x="140" y="62" width="24" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="152.0" y="78.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">b</text>
<rect x="164" y="62" width="24" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="176.0" y="78.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">c</text>
<text x="200" y="78" text-anchor="start" font-size="12" font-family="ui-monospace,Menlo,monospace" style="fill:var(--accent,#3b6fd4)">→ daba</text>
<rect x="20" y="98" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="32.0" y="114.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">d</text>
<rect x="44" y="98" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56.0" y="114.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">a</text>
<rect x="68" y="98" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="114.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">b</text>
<rect x="92" y="98" width="24" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="104.0" y="114.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">a</text>
<rect x="116" y="98" width="24" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="128.0" y="114.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">b</text>
<rect x="140" y="98" width="24" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="152.0" y="114.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">c</text>
<text x="200" y="114" text-anchor="start" font-size="12" font-family="ui-monospace,Menlo,monospace" style="fill:var(--accent,#3b6fd4)">→ dab</text>
<text x="20" y="140" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">栈顶拼出 abc 就整段弹掉</text>
</svg>

```python
def remove_occurrences(s, part):
    st, k = [], len(part)
    for c in s:
        st.append(c)
        # 栈顶拼出 part 就整段弹掉，新暴露的前缀还能再拼
        if len(st) >= k and "".join(st[-k:]) == part:
            del st[-k:]
    return "".join(st)
```

**复杂度。** 时间 `O(n·m)`，`m = len(part)`；空间 `O(n)`。

**易错点。**
- 只扫一遍 `replace`：删掉一段后两边拼起来会出现新的 `part`，如 `"daabcbaabcbc"` 要删三次。
- 只在压入时比较最后一个字符：必须比较整个栈顶 `k` 个字符。

**追问。**
- 为什么栈的结果等于「每次删最左边」？：栈按从左到右的顺序在第一时间删掉最早完成的那次出现，与反复删最左的结果相同。
- `part` 很长要更快？：栈里同时存 KMP 的匹配长度，每压入一个字符 `O(1)` 均摊更新，总 `O(n + m)`。

**同模式。** LC 20 有效的括号、LC 1047 删除字符串中的所有相邻重复项、LC 1209 删除字符串中的所有相邻重复项 II、LC 2390 从字符串中移除星号
