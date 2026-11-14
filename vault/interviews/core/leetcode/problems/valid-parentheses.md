---
slug: valid-parentheses
---
## Q
**LC 20 有效的括号**｜Easy

判断只含 `()[]{}` 的字符串是否有效：括号类型匹配，且按正确顺序闭合。

## A
**一句话。** 栈：左括号入栈，右括号必须和栈顶配对才弹出，扫完栈要为空。

**图解。** 每个字符处理后的栈：右括号与栈顶配对就弹出，扫完栈空即有效。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 156">
<rect x="40" y="14" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60.0" y="31.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">(</text>
<rect x="80" y="14" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100.0" y="31.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">[</text>
<rect x="120" y="14" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140.0" y="31.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">{</text>
<rect x="160" y="14" width="40" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="180.0" y="31.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">}</text>
<rect x="200" y="14" width="40" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="220.0" y="31.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">]</text>
<rect x="240" y="14" width="40" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="260.0" y="31.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">)</text>
<text x="32" y="31" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s</text>
<text x="32" y="100" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">栈</text>
<line x1="40" y1="130" x2="280" y2="130" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="47.0" y="110" width="26" height="20" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="60.0" y="124" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">(</text>
<rect x="87.0" y="110" width="26" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100.0" y="124" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">(</text>
<rect x="87.0" y="90" width="26" height="20" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="100.0" y="104" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">[</text>
<rect x="127.0" y="110" width="26" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140.0" y="124" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">(</text>
<rect x="127.0" y="90" width="26" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140.0" y="104" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">[</text>
<rect x="127.0" y="70" width="26" height="20" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="140.0" y="84" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">{</text>
<rect x="167.0" y="110" width="26" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="180.0" y="124" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">(</text>
<rect x="167.0" y="90" width="26" height="20" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="180.0" y="104" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">[</text>
<rect x="207.0" y="110" width="26" height="20" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="220.0" y="124" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">(</text>
<text x="260.0" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">空</text>
<text x="160" y="150" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">右括号与栈顶配对就弹出</text>
</svg>

```python
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False     # 栈空或类型对不上
        else:
            stack.append(ch)
    return not stack             # 还有没闭合的左括号
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只数三种括号个数是否相等：`"([)]"` 会被判有效。
- 弹栈前不判空：`"]"` 对空栈 `pop()` 抛 `IndexError`。
- 结尾不查栈空：`"(("` 扫完无错却未闭合。

**追问。**
- 要返回第一个出错的位置？：栈里存下标，出错时返回当前下标，或结束后栈底的下标。
- 只有一种括号？：栈退化成计数器，空间 `O(1)`，计数不能为负。

**同模式。** LC 22 括号生成、LC 32 最长有效括号、LC 921 使括号有效的最少添加、LC 1249 移除无效的括号
