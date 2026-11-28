---
id: lct-learn-binary-search-2-3
node: binary-search.2.3
type: qa
step: 1
---
## Q
**二分算法 › 二分答案 › 二分间接值**｜学习卡

套路是什么？

## A
**一句话。** 答案是个总和，不好直接二分，就二分一个间接值——水位线 `t`：`t` 越低取走的件数越多（单调），二分出最小的 `t` 使取走件数不超过预算，再补上水位以上的等差数列和与剩余订单。

下图：LC 1648（inventory = [2,5]，orders = 4），二分的是水位线 `t`，答案 = 5+4+3+2 = 14。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<rect x="60" y="108" width="50" height="22" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="85" y="123" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="60" y="86" width="50" height="22" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="85" y="101" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="130" y="108" width="50" height="22" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="155" y="123" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="130" y="86" width="50" height="22" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="155" y="101" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="130" y="64" width="50" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="155" y="79" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="130" y="42" width="50" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="155" y="57" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<rect x="130" y="20" width="50" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="155" y="35" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5</text>
<line x1="40" y1="86" x2="200" y2="86" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<text x="205" y="90" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">水位 t = 2</text>
<line x1="40" y1="130" x2="200" y2="130" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="205" y="34" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">取走 &gt; t 的部分：5 4 3</text>
<text x="205" y="50" text-anchor="start" font-size="10" font-family="sans-serif" fill="currentColor">cnt(t) = 3 ≤ orders = 4</text>
<text x="205" y="112" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">剩 1 单按价 t = 2 卖</text>
<text x="170" y="156" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">t 越低取走越多：二分最小的 t 使 cnt(t) ≤ orders</text>
</svg>

```python
def max_profit(inventory, orders):  # LC 1648
    def cnt(t):                     # 取走所有 > t 的部分共多少件
        return sum(max(a - t, 0) for a in inventory)

    left, right = -1, max(inventory)    # cnt(max) = 0，一定可行
    while left + 1 < right:         # 最小的 t 使 cnt <= orders
        mid = (left + right) // 2
        if cnt(mid) <= orders:
            right = mid
        else:
            left = mid
    t = right
    ans = 0
    for a in inventory:
        if a > t:                   # 取走 a, a-1, ..., t+1
            ans += (a + t + 1) * (a - t) // 2
    ans += (orders - cnt(t)) * t    # 剩下的订单都卖水位 t 的球
    return ans % (10**9 + 7)
```

**要点。**
- 为什么对？：贪心总是卖当前最贵的球，等价于把所有高于某个水位的球全卖掉；`cnt(t)` 随 `t` 单调不增，所以能二分。
- 为什么要最小的 `t`？：水位偏高时，水位上的球不够补剩余订单；最小的 `t` 保证 `orders - cnt(t)` 个订单刚好能用价值 `t` 的球补上。
- 返回值是二分结果吗？：不是，二分的是间接值 `t`，答案要用 `t` 再算一步。

**易错点。**
- 漏掉剩余订单：`inventory = [2,5]`、`orders = 4` 应得 `14`，漏了得到 `12`。
- 取模过早：等差数列和先算精确值再取模，`(a+t+1)*(a-t)//2` 不能先对分子取模再除。
- 逐个卖球：`inventory = [10**9]`、`orders = 10**9` 必须用求和公式。

**对应题目。** LC 1648 销售价值减少的颜色球
