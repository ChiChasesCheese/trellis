---
slug: maximum-number-of-non-overlapping-substrings
---
## Q
**LC 1520 最多的不重叠子字符串**｜Hard

小写字符串 `s`，选出最多个互不重叠的子串，要求子串里出现的每个字符，在 `s` 中的所有出现都在这个子串里。数目相同时取总长度最小的方案，任意顺序返回。

## A
**一句话。** 每个字符 `c` 从首次出现处向右扩成「闭包」区间（扩到能装下区间内所有字符的全部出现，若需要向左扩就作废）；这些区间要么嵌套要么不相交，按右端点贪心选不重叠的，自然选到最短的。

**图解。** `"adefaddaccc"`：`a` 的闭包是整个 `adefadda`，`e`、`f` 各自一格，`c` 是 `ccc`；按右端贪心选出 `e`、`f`、`ccc`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 354 142">
<text x="66" y="26.9" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s</text>
<text x="86.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">a</text>
<text x="110.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d</text>
<text x="134.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">e</text>
<text x="158.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f</text>
<text x="182.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">a</text>
<text x="206.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d</text>
<text x="230.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">d</text>
<text x="254.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">a</text>
<text x="278.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">c</text>
<text x="302.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">c</text>
<text x="326.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">c</text>
<text x="66" y="54.9" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a 的闭包</text>
<rect x="74" y="40" width="24" height="24" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<rect x="98" y="40" width="24" height="24" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<rect x="122" y="40" width="24" height="24" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<rect x="146" y="40" width="24" height="24" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="40" width="24" height="24" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<rect x="194" y="40" width="24" height="24" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<rect x="218" y="40" width="24" height="24" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<rect x="242" y="40" width="24" height="24" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<rect x="266" y="40" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="290" y="40" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="314" y="40" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="66" y="82.9" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">选中</text>
<rect x="74" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="98" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="122" y="68" width="24" height="24" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="146" y="68" width="24" height="24" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="194" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="218" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="242" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="266" y="68" width="24" height="24" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="290" y="68" width="24" height="24" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="314" y="68" width="24" height="24" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="16" y="106" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a 的闭包是下标 0..7，包含 e、f 的闭包</text>
<text x="16" y="124" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">按右端贪心：e、f、ccc 共 3 个</text>
</svg>

```python
def max_num_of_substrings(s):
    first, last = {}, {}
    for i, c in enumerate(s):
        first.setdefault(c, i)
        last[c] = i
    segs = []
    for c in first:
        l, r = first[c], last[c]
        i, ok = l, True
        while i <= r:          # 把区间内字符的全部出现包进来
            if first[s[i]] < l:
                ok = False     # 要向左扩：由更左的字符负责
                break
            r = max(r, last[s[i]])
            i += 1
        if ok:
            segs.append((r, l))
    segs.sort()                # 按右端点
    ans, end = [], -1
    for r, l in segs:
        if l > end:            # 不重叠就选
            ans.append(s[l:r + 1])
            end = r
    return ans
```

**复杂度。** 时间 `O(26·n)`，空间 `O(26)`（不计输出）。

**易错点。**
- 只用 `[first[c], last[c]]` 不再扩：区间里其他字符可能伸到外面，`"abab"` 中 `a` 的区间必须扩到 `b` 的最后一次出现。
- 按左端点或长度贪心：嵌套时要选里面那个，按右端点排序正好先遇到内层。

**追问。**
- 为什么候选区间只会嵌套或不相交？：若两个闭包部分重叠，重叠处的字符会把两者都扩成包含对方，矛盾。
- 为什么按右端贪心同时保证总长最小？：每次选的都是右端最早的，也就是最内层的那个，数目最多且每个都最短。

**同模式。** LC 763 划分字母区间、LC 435 无重叠区间
