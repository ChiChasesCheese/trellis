---
id: lct-learn-string-3
node: string.3
type: qa
step: 1
---
## Q
**字符串 › Manacher 算法（回文串）**｜学习卡

套路是什么？

## A
**一句话。** 字符间插入 `#` 把奇偶回文统一成奇回文，维护「最靠右的回文盒子」`[m - hl, r]`，新中心先抄镜像位置的半径，再向外暴力扩，整体 `O(n)`；中心 `i` 的半径 `hl[i]` 恰好等于它在原串里的回文长度。

下图：维护最靠右的回文盒子，盒内的新中心直接借用对称位置的半径。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="15" y="50" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="29.0" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">#</text>
<rect x="43" y="50" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="57.0" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a</text>
<rect x="71" y="50" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">#</text>
<rect x="99" y="50" width="28" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="113.0" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">b</text>
<rect x="127" y="50" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="141.0" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">#</text>
<rect x="155" y="50" width="28" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="169.0" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a</text>
<rect x="183" y="50" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="197.0" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">#</text>
<rect x="211" y="50" width="28" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="225.0" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">b</text>
<rect x="239" y="50" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="253.0" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">#</text>
<rect x="267" y="50" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="281.0" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a</text>
<rect x="295" y="50" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="309.0" y="68.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">#</text>
<line x1="43.0" y1="44" x2="43.0" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="295.0" y1="44" x2="295.0" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="43.0" y1="44" x2="295.0" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="169.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">回文盒子 [m - hl, r]</text>
<line x1="169.0" y1="94" x2="169.0" y2="80" stroke-width="1.2" stroke="currentColor"/>
<polygon points="169.0,80.0 172.0,86.3 166.0,86.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="169.0" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">m</text>
<line x1="225.0" y1="94" x2="225.0" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="225.0,80.0 228.0,86.3 222.0,86.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="225.0" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<line x1="113.0" y1="94" x2="113.0" y2="80" stroke-width="1.2" stroke="currentColor"/>
<polygon points="113.0,80.0 116.0,86.3 110.0,86.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="113.0" y="108" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2m - i</text>
<text x="170" y="136" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">i 在盒子内：先抄镜像的半径（不越过 r），再向外暴力扩</text>
<text x="170" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">插 # 后奇偶回文统一；r 只右移，整体 O(n)</text>
</svg>

```python
def manacher(s):
    t = "^#" + "#".join(s) + "#$"    # 哨兵 ^ $ 免去越界判断
    hl = [0] * len(t)                # hl[i]：以 t[i] 为中心的半径
    m = r = 0                        # 盒子中心 m 与右端 r
    for i in range(1, len(t) - 1):
        if i < r:                    # 镜像位置 2m-i 的半径不能越盒
            hl[i] = min(r - i, hl[2 * m - i])
        while t[i - hl[i] - 1] == t[i + hl[i] + 1]:
            hl[i] += 1               # 继续向外扩，右端 r 只右移
        if i + hl[i] > r:
            m, r = i, i + hl[i]
    return hl                        # hl[i] 即原串中的回文长度
```

**要点。**
- 为什么对？：盒子内的回文关于 `m` 对称，`i` 的镜像位置已有答案，最多抄到盒边界；只有越过 `r` 才需要真实比较，而每次比较成功都让 `r` 右移，总比较次数 `O(n)`。
- LC 5 怎么改？：取 `hl` 最大的中心 `i`，起点是 `(i - hl[i]) // 2`，长度是 `hl[i]`。
- LC 647 怎么改？：中心 `i` 贡献 `(hl[i] + 1) // 2` 个回文子串，累加即答案。
- 判断 `s[l:r]` 是否回文怎么改？：对应中心下标是 `l + r + 1`，`hl[l + r + 1] >= r - l` 即可。

**易错点。**
- 忘了哨兵：`t` 两端没有 `^`、`$` 会越界，`while` 里要多写边界判断。
- 起点公式写成 `i - hl`：t 中的下标要除以 `2` 才是原串下标，`"abba"` 的中心在 `#`，应得起点 `0`。
- 用 `hl[i]` 当 t 里的长度：它已经是原串回文长度，不用再减一。

**对应题目。** LC 5 最长回文子串、LC 647 回文子串
