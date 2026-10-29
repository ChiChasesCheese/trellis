---
id: uth-java-string-2-hashcode
node: java.string
type: qa
step: 2
---
## Q
**String 的 hashCode 怎么算、会重复算吗**｜Java · OpenJDK 25

`"Aa"` 和 `"BB"` 的 `hashCode` 为什么相同？`String` 每次调用 `hashCode()` 都重新计算吗？

## A
**背景。** 字符串要当 `HashMap` 的 key，就得有 `hashCode`，而且相同内容的字符串必须算出相同的数。最简单的做法是把每个字符的编码按位置「加权」叠起来。

**结构。** 多项式哈希：`h = 31*h + 字符`，从左到右累加，即 `s[0]*31^(n-1) + … + s[n-1]`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="14" y="26" width="44" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="36" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Aa</text>
<line x1="58" y1="40" x2="80" y2="40" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,40.0 76.0,42.0 76.0,38.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="84" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">65*31+97</text>
<rect x="14" y="96" width="44" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="36" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">BB</text>
<line x1="58" y1="110" x2="80" y2="110" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,110.0 76.0,112.0 76.0,108.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="84" y="114" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">66*31+66</text>
<rect x="250" y="62" width="70" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="285" y="83" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2112</text>
<line x1="158" y1="40" x2="248" y2="72" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="248.0,72.0 242.5,72.7 244.1,68.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="158" y1="110" x2="248" y2="88" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="248.0,88.0 243.7,91.6 242.5,86.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">h = 31*h + 字符 不同的串可能撞</text>
</svg>
```

**细节。**

- 实测 `"Aa".hashCode()` 与 `"BB".hashCode()` 都是 2112：`65*31+97 = 66*31+66`。
- 算出后缓存在 `hash` 字段里，字符串不可变，所以缓存永远有效。
- 结果恰好为 0（包括空串）时不写缓存，而是置 `hashIsZero = true`，避免反复重算。

**为什么。** 不可变换来哈希可缓存，所以 `String` 当 `HashMap` 的 key 很便宜；代价是容易构造冲突，因此 `HashMap` 要有红黑树兜底。

**例题：** LC 1044 最长重复子串

给字符串 `s`，返回任意一个最长的重复子串（在 `s` 中出现两次或更多次，出现可以重叠），没有就返回 `""`。`2 <= s.length <= 3 * 10^4`，小写字母。例：`"banana"` 返回 `"ana"`。

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
