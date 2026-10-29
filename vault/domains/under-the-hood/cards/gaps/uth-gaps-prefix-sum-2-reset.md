---
id: uth-gaps-prefix-sum-2-reset
node: gaps.prefix-sum
type: qa
step: 2
---
## Q
**进程重启，累计数归零怎么办**｜Prometheus · v3.5 rate()

服务重启后计数器从 0 重新数，窗口里最后一个值比第一个还小。`rate()` 怎样不算出负数？

## A
**结构。** 先算「最后 − 第一」，再从头扫一遍样本：只要某个值比前一个小，就认定中间重启过，把变小前的那个值补回去。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<line x1="20" y1="150" x2="300" y2="150" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="34" y1="60" x2="88" y2="51" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="88" y1="51" x2="142" y2="42" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="142" y1="42" x2="196" y2="145.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="196" y1="145.5" x2="250" y2="136.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="34" cy="60" r="3.5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="34" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">100</text>
<circle cx="88" cy="51" r="3.5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="88" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">110</text>
<circle cx="142" cy="42" r="3.5" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="142" y="33" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">120</text>
<circle cx="196" cy="145.5" r="3.5" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="196" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<circle cx="250" cy="136.5" r="3.5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="250" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">15</text>
<text x="172" y="78" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">重启 归零</text>
</svg>
```

```python
total = last - first
for prev, cur in pairwise(samples):
    if cur < prev:       # 变小 = 重启归零
        total += prev    # 补回重启前的累计值
```

例：`100, 110, 120, 5, 15`。最后 − 第一 = 15 − 100 = −85；120 → 5 变小，补 120，得 35 = 10 + 10 + 5 + 10。

**细节。**

- 上面是 v3.5 `extrapolatedRate` 里那段循环的等价写法
- 重启后的 5 被当作「从 0 涨上来的」，全部计入增量
- 只看「比前一个小」：两次采集之间重启、又涨回原值以上，发现不了

**坑。** 多个实例要先 `rate()` 再 `sum()`。先求和，一个实例归零的下降会被别的实例的上涨盖住，`rate()` 就认不出重启了（官方文档）。

**对应 LeetCode：** 无直接对应的题
