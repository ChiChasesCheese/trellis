---
id: uth-devtools-compression-1-deflate
node: devtools.compression
type: qa
step: 1
---
## Q
**gzip 怎么把重复的文本压小**｜DEFLATE · zlib 1.3.2

`abcabcabc` 这样的重复内容，gzip 怎样用更少的空间存下来？

## A
**背景。** 压缩的第一个想法：出现过的内容不必再写一遍，只写“往回看多远、照抄多长”。`abcabcabc` 的后 6 个字符前面已经出现过，所以可以写成 `abc` 加一条指令「往回 3 个、复制 6 个」：9 个字符变成 3 个字符加一对数。这个办法叫 LZ77。

**结构。** DEFLATE（gzip、zip、PNG 用的格式）分两步：先用 LZ77 在最近 32 KB 里找重复串，换成（距离，长度）；再对没被替换的原字符和这些（距离，长度）做哈夫曼编码（让常出现的符号用更短的码）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="44" y="66" width="28" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a</text>
<rect x="72" y="66" width="28" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b</text>
<rect x="100" y="66" width="28" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="114" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c</text>
<rect x="128" y="66" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="142" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a</text>
<rect x="156" y="66" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b</text>
<rect x="184" y="66" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="198" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c</text>
<rect x="212" y="66" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="226" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a</text>
<rect x="240" y="66" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="254" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b</text>
<rect x="268" y="66" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="282" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c</text>
<path d="M142,66 Q100,18 61.3,62.2" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M58.0,66.0 L60.0,58.8 L64.9,63.1 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="100" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">往回 3 个</text>
<line x1="128" y1="106" x2="296" y2="106" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">复制 6 个</text>
<line x1="170" y1="134" x2="170" y2="149" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M170.0,154.0 L166.7,147.2 L173.3,147.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<rect x="70" y="160" width="70" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">abc</text>
<text x="155" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">+</text>
<rect x="170" y="160" width="100" height="28" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="220" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">往回 3 复制 6</text>
<text x="170" y="208" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">9 个字符变成 3 个字符加一对数</text>
</svg>
```

**细节。**

- 距离 1 到 32768，长度 3 到 258
- 怎样找重复：zlib（gzip 背后的压缩库）以 3 个字节为键建哈希表，同一个键的历史位置串成一条链，到时沿链找候选
- 默认级别 6 最多沿链找 128 个候选，级别 9 是 4096：找得越多，越可能找到更长的重复，压得更小，也更慢

**为什么。** 窗口只有 32 KB，找匹配快、内存少，代价是看不到更远的重复。

**例题：** LC 1044 最长重复子串

返回字符串 `s` 中最长的重复子串（在 `s` 里出现 2 次或更多次，出现之间可以重叠），没有则返回 `""`。`s` 只含小写字母，`2 <= s.length <= 3 * 10^4`。例：`"banana"` → `"ana"`。

```python
import random


def longest_dup_substring(s: str) -> str:
    n = len(s)
    nums = [ord(c) - 96 for c in s]        # 'a'..'z' -> 1..26
    mod = (1 << 61) - 1
    base = random.randrange(1 << 20, mod)  # 随机底数：防止被构造数据卡哈希

    def find(length: int) -> int:          # 返回某个长度为 length 的重复子串的起点，没有则 -1
        top = pow(base, length, mod)       # base^length，用来滚掉最左边的字符
        h = 0
        for x in nums[:length]:
            h = (h * base + x) % mod
        seen = {h: [0]}                    # 哈希 -> 起点列表（链式，应对碰撞）
        for i in range(1, n - length + 1):
            h = (h * base - nums[i - 1] * top + nums[i + length - 1]) % mod
            for j in seen.get(h, ()):
                if s[j:j + length] == s[i:i + length]:     # 哈希相同再逐字比对，杜绝假阳性
                    return i
            seen.setdefault(h, []).append(i)
        return -1

    lo, hi, start = 1, n - 1, -1           # 答案长度在 [0, n-1]；"有长度 L 的重复" 对 L 单调
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if (idx := find(mid)) != -1:
            start, best, lo = idx, mid, mid + 1
        else:
            hi = mid - 1
    return s[start:start + best] if best else ""
```
