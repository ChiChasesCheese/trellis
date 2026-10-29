---
id: uth-python-set-2-hash-seed
node: python.set
type: qa
step: 2
---
## Q
**字符串集合的顺序为什么每次运行都不同**｜Python · CPython 3.14

同一段代码 `print(list({'apple','banana','cherry','date'}))` 连续跑几次，输出顺序为什么会变？

## A
**背景。** 集合遍历的顺序就是元素在表里的槽顺序，而槽号由哈希值决定。如果哈希算法固定，攻击者能提前造出一批哈希相同的字符串，把表拖成 O(n²)（哈希洪水，hash flooding）。所以哈希里掺进了一个每次启动随机生成的密钥。

**结构。** `str` 和 `bytes` 的哈希是带密钥的 SipHash（3.14 默认 `siphash13`），密钥在进程启动时随机生成。哈希变了，元素落进的槽就变了，遍历顺序随之改变。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="14" y="48" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第1次</text>
<rect x="70" y="30" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="100" y="30" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="115" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="130" y="30" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="160" y="30" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="190" y="30" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="205" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="220" y="30" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="250" y="30" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="265" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="280" y="30" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="295" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<text x="190" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">遍历顺序 a b c d</text>
<text x="14" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第2次</text>
<rect x="70" y="100" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="85" y="117" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="100" y="100" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="130" y="100" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="145" y="117" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="160" y="100" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="175" y="117" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<rect x="190" y="100" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="220" y="100" width="30" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="235" y="117" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="250" y="100" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="280" y="100" width="30" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">遍历顺序 c a d b</text>
<text x="170" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">密钥每次启动随机 同样的词落进不同的槽</text>
</svg>
```

**细节。**

- 实测三次输出三种顺序。
- `PYTHONHASHSEED=0` 关闭随机化，两次输出相同。
- `int` 不随机，小整数集合的顺序每次相同，但也不能依赖它。

**为什么。** 密钥保密，攻击者就无法预先构造哈希相同的字符串。

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
