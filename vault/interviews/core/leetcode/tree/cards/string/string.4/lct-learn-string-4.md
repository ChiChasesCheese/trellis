---
id: lct-learn-string-4
node: string.4
type: qa
step: 1
---
## Q
**字符串 › 字符串哈希**｜学习卡

套路是什么？

## A
**一句话。** 字符串哈希：把窗口当成 `B` 进制数，右移时「乘 `B` 加进、减掉滚出的那位」`O(1)` 更新；对长度二分，每个长度扫一遍找重复窗口。

下图：窗口当作 `B` 进制数，右移一格 `O(1)` 更新哈希。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="30" y="50" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="53.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="76" y="50" width="46" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="99.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a</text>
<rect x="122" y="50" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="145.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">n</text>
<rect x="168" y="50" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="191.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="214" y="50" width="46" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="237.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">n</text>
<rect x="260" y="50" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="283.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="122.0" y1="44" x2="122.0" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="260.0" y1="44" x2="260.0" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="122.0" y1="44" x2="260.0" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="191.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">窗口 L = 3</text>
<line x1="237.0" y1="96" x2="237.0" y2="82" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="237.0,82.0 240.0,88.3 234.0,88.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="237.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">滚入：h·B + c</text>
<line x1="99.0" y1="96" x2="99.0" y2="82" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="99.0,82.0 102.0,88.3 96.0,88.3" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="99.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">滚出：- c·B^L</text>
<text x="170" y="140" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">每个 L 扫一遍 O(n)；有长 L 的重复必有 L-1 → 二分 L</text>
</svg>

```python
def longest_dup_substring(s):
    M = (1 << 61) - 1
    B = random.randrange(10**6, M)   # 随机底数防卡哈希
    def find(L):                     # 长 L 重复窗口的起点，无则 -1
        top, h, seen = pow(B, L, M), 0, {}
        for i, c in enumerate(s):
            h = (h * B + ord(c)) % M           # 滚入
            if i >= L:
                h = (h - ord(s[i - L]) * top) % M   # 滚出
            if i >= L - 1:
                if h in seen: return seen[h]   # 求稳可再比对
                seen[h] = i - L + 1
        return -1
    lo, hi, ans = 1, len(s) - 1, ""
    while lo <= hi:                  # 有长 L 的重复必有长 L-1 的
        mid = (lo + hi) // 2
        st = find(mid)
        if st >= 0: ans, lo = s[st:st + mid], mid + 1
        else: hi = mid - 1
    return ans
```

**要点。**
- 为什么对？：哈希窗口 `O(1)` 滚动，一个长度 `O(n)` 判定；判定对长度单调（有长 `L` 的重复必有长 `L - 1` 的），所以二分。
- LC 1062 怎么改？：返回最大的可行长度 `mid` 而不是子串。
- LC 187 怎么改？：窗口定长 `10`，不用二分：每个碱基编 `2` 位，窗口是 `20` 位整数，`& mask` 去掉最老的，计数到第二次时收集。

**易错点。**
- 以为两次出现不能重叠：`"banana"` 的 `"ana"` 就共用一个 `a`，答案会少 `1`。
- `find` 只返回布尔值：二分结束时取不出子串，要返回起点。
- LC 187 用 `>= 2` 收集：`"AAAAAAAAAAAAA"` 会收集 `3` 次，应只有 `1` 个，要恰好 `== 2`。

**对应题目。** LC 187 重复的DNA序列、LC 1044 最长重复子串、LC 1062 最长重复子串
