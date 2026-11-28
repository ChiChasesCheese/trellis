---
id: lct-learn-greedy-1-7
node: greedy.1.7
type: qa
step: 1
---
## Q
**贪心算法 › 贪心策略 › 交换论证法**｜学习卡

套路是什么？

## A
**一句话。** 交换论证：相邻两项若换位更优就换，最优排列里任意相邻对都不能再换；这个相邻关系可传递，所以能直接写成排序比较器。

下图：LC 179，只看相邻两项换不换更优，就得到整个排序的比较规则。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<text x="20" y="30" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">相邻两项 a、b：比较两种拼法</text>
<rect x="20" y="44" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="40.0" y="62.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="60" y="44" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="62.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30</text>
<text x="112" y="63" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ "330"</text>
<rect x="190" y="44" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210.0" y="62.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30</text>
<rect x="230" y="44" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250.0" y="62.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="282" y="63" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">→ "303"</text>
<text x="170" y="98" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a + b &gt; b + a：a 排前面；这个关系可传递</text>
<text x="170" y="118" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 直接当排序比较器：9 5 34 3 30</text>
</svg>

```python
def largest_number(nums):
    def cmp(a, b):               # a + b 拼出来更大，a 就排前面
        return (a + b < b + a) - (a + b > b + a)

    s = sorted(map(str, nums), key=cmp_to_key(cmp))
    return "0" if s[0] == "0" else "".join(s)   # 全零只留一个
```

**要点。**
- 为什么对？：交换论证：若相邻 `a, b` 满足 `a+b < b+a`，换成 `b, a` 整串变大，所以最优排列里每个相邻对都是 `a+b >= b+a`；该关系可传递，排序就能得到全局最优。
- 不想写比较器怎么办？：每个数不超过 `10` 位，按 `s * 10` 的字典序降序排，等价。
- 要最小的拼接数怎么改？：比较方向反过来，注意前导零的题意。

**易错点。**
- 按字典序降序排：`[3,30]` 得 `"303"`，应为 `"330"`。
- 全零不特判：`[0,0]` 拼出 `"00"`，应为 `"0"`。
- 比较器返回布尔值：`cmp_to_key` 要负 / 零 / 正的整数。

**对应题目。** LC 179 最大数
