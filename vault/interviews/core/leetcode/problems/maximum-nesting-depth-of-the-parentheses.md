---
slug: maximum-nesting-depth-of-the-parentheses
---
## Q
**LC 1614 括号的最大嵌套深度**｜Easy

给一个括号匹配合法的表达式字符串，返回括号的最大嵌套深度。

## A
**一句话。** 计数器代替栈：遇 `(` 加一并更新最大值，遇 `)` 减一，其他字符跳过。

**图解。** 折线是扫描时的深度计数器，它的最高点就是答案。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 135">
<line x1="18" y1="32" x2="303" y2="32" stroke-width="1" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<text x="303" y="27" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">best = 3</text>
<polyline points="18,92 18,72 33,72 33,72 48,72 48,72 63,72 63,52 78,52 78,52 93,52 93,52 108,52 108,52 123,52 123,72 138,72 138,72 153,72 153,52 168,52 168,32 183,32 183,32 198,32 198,52 213,52 213,52 228,52 228,52 243,52 243,72 258,72 258,92 273,92 273,92 288,92 288,92 303,92" fill="none" stroke-width="1.6" stroke="currentColor"/>
<text x="10" y="96" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="10" y="76" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="10" y="56" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="10" y="36" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="25.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">(</text>
<text x="40.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">1</text>
<text x="55.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">+</text>
<text x="70.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">(</text>
<text x="85.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">2</text>
<text x="100.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">*</text>
<text x="115.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">3</text>
<text x="130.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">)</text>
<text x="145.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">+</text>
<text x="160.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">(</text>
<text x="175.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">(</text>
<text x="190.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">8</text>
<text x="205.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">)</text>
<text x="220.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">/</text>
<text x="235.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">4</text>
<text x="250.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">)</text>
<text x="265.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">)</text>
<text x="280.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">+</text>
<text x="295.5" y="116" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">1</text>
<text x="160" y="131" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">折线：读完该字符后的深度</text>
</svg>

```python
def max_depth(s):
    depth = best = 0
    for c in s:
        if c == "(":
            depth += 1
            best = max(best, depth)
        elif c == ")":
            depth -= 1
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 在 `)` 时更新最大值：深度已经减了，会少算一层。

**追问。**
- 为什么不用栈？：只有一种括号且已保证合法，栈里只会是 `(`，栈的高度就是计数器。
- 输入可能不合法？：计数器变负或最后不为零就是不合法；多种括号就得用真正的栈。

**同模式。** LC 20 有效的括号、LC 1021 删除最外层的括号、LC 32 最长有效括号
