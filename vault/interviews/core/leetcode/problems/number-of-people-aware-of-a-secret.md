---
slug: number-of-people-aware-of-a-secret
---
## Q
**LC 2327 知道秘密的人数**｜Medium

第 1 天一个人知道秘密。每人在知道后第 `delay` 天起每天告诉一个新人，在第 `forget` 天忘记（当天起不再分享）。求第 `n` 天结束时知道秘密的人数，对 `10^9+7` 取余。

## A
**一句话。** `f[i]` 记第 `i` 天新知道的人数；能在第 `i` 天分享的是第 `(i-forget, i-delay]` 天知道的人，用一个滑动和 `share` 维护；答案是最后 `forget` 天的 `f` 之和。

**图解。** `delay=2, forget=4`：第 6 天时第 3 到 6 天新知道的人还记得，`1+1+1+2 = 5`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 144">
<text x="54" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第几天</text>
<text x="77.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="107.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="137.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<text x="167.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<text x="197.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5</text>
<text x="227.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6</text>
<text x="54" y="64.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新知道</text>
<rect x="62" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="77.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="92" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="107.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="122" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="137.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="152" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="167.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="182" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="197.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="212" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="227.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="16" y="90" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">深色：第 6 天仍记得秘密的人</text>
<text x="16" y="108" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 1、2 天知道的人已在第 5、6 天忘了</text>
<text x="16" y="126" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor" font-weight="600">答案 1 + 1 + 1 + 2 = 5</text>
</svg>

```python
def people_aware_of_secret(n, delay, forget):
    MOD = 10**9 + 7
    f = [0] * (n + 1)          # f[i]：第 i 天新知道的人数
    f[1] = 1
    share = 0                  # 第 i 天能分享的人数
    for i in range(2, n + 1):
        if i - delay >= 1:
            share += f[i - delay]    # 到了能分享的日子
        if i - forget >= 1:
            share -= f[i - forget]   # 今天忘了
        f[i] = share % MOD
    return sum(f[n - forget + 1:]) % MOD
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 按「知道秘密的总人数」递推：要分清新知道的、能分享的、已忘记的，用「新增人数」做状态最清楚。
- 答案把 `f` 全加起来：第 `n - forget` 天及以前知道的人已经忘了。

**追问。**
- 不用滑动和？：每天直接把 `f[i-forget+1 .. i-delay]` 加一遍，`O(n·forget)`，`n <= 1000` 也能过。
- 问第 `n` 天能分享秘密的人数？：就是循环结束时的 `share`。

**同模式。** LC 70 爬楼梯、LC 1155 掷骰子等于目标和的方法数、LC 629 K 个逆序对数组
