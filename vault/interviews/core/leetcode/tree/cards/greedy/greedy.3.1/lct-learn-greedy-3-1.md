---
id: lct-learn-greedy-3-1
node: greedy.3.1
type: qa
step: 1
---
## Q
**贪心算法 › 字符串贪心 › 字典序最小/最大**｜学习卡

套路是什么？

## A
**一句话。** 字典序贪心：高位权重大，从左往右让每一位尽量大（小），并把需要的交换放在尽量靠后的位置，免得伤到前面。

下图：LC 670，从最高位起找右边最大的数字，有并列取最右的。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<rect x="70" y="40" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="95.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="120" y="40" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="170" y="40" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="195.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">9</text>
<rect x="220" y="40" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<path d="M 95.0 68 Q 145.0 100 195.0 68" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="195.0,68.0 193.2,74.8 188.6,70.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="95.0" y="32" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<text x="170" y="112" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">高位优先：右边有更大的数就换，换最右的那个 → 9913</text>
<text x="170" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">小数被换到尽量靠后，伤害最小</text>
</svg>

```python
def maximum_swap(num):           # 至多交换一次，求最大值
    s = list(str(num))
    last = {c: i for i, c in enumerate(s)}   # 每个数字最后出现的位置
    for i, c in enumerate(s):
        for big in "9876543210":     # 从最大的数字找起
            if big <= c:             # 右边不会再有更大的
                break
            if last.get(big, -1) > i:
                j = last[big]        # 换最右一个：小数落得更靠后
                s[i], s[j] = s[j], s[i]
                return int("".join(s))
    return num
```

**要点。**
- 为什么对？：第一个右边存在更大数字的位置，是能被提升的最高位；换成最大的数字最划算，且取它最右的一次出现，让被换下去的小数落在尽量低位。
- LC 2948 怎么改？：按值排序，相邻值差 `<= limit` 连成一组（连通可传递），组内位置升序对应值升序，靠前的位置拿小值。
- LC 3474 怎么改？：先铺所有 `'T'` 窗口（重叠处冲突则无解），自由位填 `'a'`；再对仍等于 `str2` 的 `'F'` 窗口，把它最右的自由位改成 `'b'`，自由位全被钉死则无解。

**易错点。**
- LC 670 换最大数字的第一次出现：`1993` 得 `9193`，应为 `9913`。
- LC 670 换完不返回：只能换一次，`2736` 继续换会得 `7632`。
- LC 3474 改最左的自由位：`("F", "aa")` 得 `"ba"`，应为 `"ab"`。

**对应题目。** LC 670 最大交换、LC 2948 交换得到字典序最小的数组、LC 3474 字典序最小的生成字符串
