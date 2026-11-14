---
slug: minimum-add-to-make-parentheses-valid
---
## Q
**LC 921 使括号有效的最少添加**｜Medium

只含 `(` 和 `)` 的字符串，每次可在任意位置插入一个括号，求使其有效的最少插入次数。

## A
**一句话。** 扫描时记未配对的 `(`，遇到没得配的 `)` 就补一个 `(`，答案是补的数加剩下的 `(`。

**图解。** 两个计数器随扫描变化：没得配的 `)` 让 `add` 加一，剩下的 `(` 最后各补一个。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 150">
<rect x="90" y="14" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110.0" y="31.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">(</text>
<rect x="130" y="14" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150.0" y="31.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">)</text>
<rect x="170" y="14" width="40" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="190.0" y="31.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">)</text>
<rect x="210" y="14" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230.0" y="31.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">(</text>
<text x="82" y="31" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s</text>
<rect x="90" y="52" width="40" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110.0" y="68.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="130" y="52" width="40" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150.0" y="68.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="170" y="52" width="40" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190.0" y="68.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="210" y="52" width="40" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230.0" y="68.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="82" y="68" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">open_cnt</text>
<rect x="90" y="84" width="40" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110.0" y="100.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="130" y="84" width="40" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150.0" y="100.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="170" y="84" width="40" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="190.0" y="100.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="210" y="84" width="40" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230.0" y="100.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="82" y="100" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">add</text>
<text x="190.0" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">没得配 → 补 (</text>
<text x="150" y="144" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">答案 = add + open_cnt = 1 + 1 = 2</text>
</svg>

```python
def min_add_to_make_valid(s):
    open_cnt = add = 0  # 未配对的 '('；必须补的 '('
    for ch in s:
        if ch == "(":
            open_cnt += 1
        elif open_cnt:
            open_cnt -= 1
        else:
            add += 1
    return add + open_cnt   # 剩下的 '(' 各补一个 ')'
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只比两种括号的个数：`")("` 得 `0`，应为 `2`，顺序也要对。
- 忘了加结尾剩下的 `open_cnt`：`"((("` 得 `0`，应为 `3`。
- 无法配对的 `)` 让计数变成负数：`")("` 先 `-1` 再 `0`，漏掉两次插入。

**追问。**
- 改成删除最少括号（LC 1249）？：同样扫描，记下无法配对的 `)` 和剩下的 `(` 的下标，删掉。
- 含通配符 `*`（LC 678）？：维护余额区间 `[lo, hi]`，`*` 让 `lo-1`、`hi+1`，`lo` 不低于 `0`，`hi` 变负就失败。

**同模式。** LC 20 有效的括号、LC 32 最长有效括号、LC 678 有效的括号字符串、LC 1541 平衡括号字符串的最少插入次数
