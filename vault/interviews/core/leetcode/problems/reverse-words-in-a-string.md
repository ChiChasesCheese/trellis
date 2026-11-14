---
slug: reverse-words-in-a-string
---
## Q
**LC 151 反转字符串中的单词**｜Medium

反转单词顺序，单词间只留一个空格，去掉首尾多余空格。

## A
**一句话。** 从右往左扫描：跳过空格，遇到单词就切下来，最后用单个空格连接。

**图解。** `i` 从右往左扫，先切下的单词排在前面。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120">
<rect x="15" y="40" width="18" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="24.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" style="fill:var(--dim,#6b7280)">·</text>
<rect x="33" y="40" width="18" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="42.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" style="fill:var(--dim,#6b7280)">·</text>
<rect x="51" y="40" width="18" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="60.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">h</text>
<rect x="69" y="40" width="18" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">e</text>
<rect x="87" y="40" width="18" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="96.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">l</text>
<rect x="105" y="40" width="18" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="114.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">l</text>
<rect x="123" y="40" width="18" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="132.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">o</text>
<rect x="141" y="40" width="18" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" style="fill:var(--dim,#6b7280)">·</text>
<rect x="159" y="40" width="18" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="168.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">w</text>
<rect x="177" y="40" width="18" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="186.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">o</text>
<rect x="195" y="40" width="18" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="204.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">r</text>
<rect x="213" y="40" width="18" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="222.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">l</text>
<rect x="231" y="40" width="18" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="240.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">d</text>
<rect x="249" y="40" width="18" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="258.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" style="fill:var(--dim,#6b7280)">·</text>
<rect x="267" y="40" width="18" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="276.0" y="55.96" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" style="fill:var(--dim,#6b7280)">·</text>
<polyline points="285,18 15,18" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="15.0,18.0 21.0,15.0 21.0,21.0" style="fill:var(--dim,#6b7280)"/>
<text x="204.0" y="30" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 先切下</text>
<text x="96.0" y="30" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 再切下</text>
<text x="150.0" y="11" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i 从右往左</text>
<text x="15" y="90" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">跳过空格，切出单词后单空格连接：</text>
<text x="15" y="110" text-anchor="start" font-size="12" font-family="ui-monospace,Menlo,monospace" style="fill:var(--accent,#3b6fd4)">"world hello"</text>
</svg>

```python
def reverse_words(s):
    words = []
    i = len(s) - 1
    while i >= 0:
        if s[i] == " ":
            i -= 1
            continue
        end = i + 1                # 单词右开边界
        while i >= 0 and s[i] != " ":
            i -= 1
        words.append(s[i + 1:end])
    return " ".join(words)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用 `s.split(" ")`：连续空格产生空串，`"  hello world  "` 得 `"  world hello  "`，应为 `"world hello"`。
- `end = i + 1` 写在内层 `while` 之后：切出空串，单词全丢。

**追问。**
- 字符数组原地 `O(1)`？：先压缩空格，整体反转，再逐词反转回来。
- 面试允许用库吗？：`" ".join(reversed(s.split()))`，`split()` 不带参数会吃掉所有空白。

**同模式。** LC 186 反转字符串中的单词 II、LC 557 反转字符串中的单词 III、LC 344 反转字符串、LC 58 最后一个单词的长度
