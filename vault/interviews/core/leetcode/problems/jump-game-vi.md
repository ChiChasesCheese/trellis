---
slug: jump-game-vi
---
## Q
**LC 1696 跳跃游戏 VI**｜Medium

从下标 0 出发，每步最多向前跳 `k` 格，到达最后一格；得分为经过的数之和，求最大得分。

## A
**一句话。** `f[i] = nums[i] + max(f[i-k .. i-1])`，窗口最大值用单调递减队列维护，整体 `O(n)`。

**图解。** 到 `i = 5` 时窗口是下标 3、4，队列 `[3, 4]` 的 `f` 值递减，队首 `f[3] = 4`，得 `f[5] = 4 + 3 = 7`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 160">
<text x="48" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下标</text>
<text x="71.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<text x="101.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="131.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="161.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<text x="191.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<text x="221.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5</text>
<text x="48" y="64.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nums</text>
<rect x="56" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="86" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="116" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="146" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="161.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="176" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="191.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-7</text>
<rect x="206" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="221.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="48" y="98.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f</text>
<rect x="56" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="86" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="116" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="146" y="80" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="161.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="176" y="80" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="191.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-3</text>
<rect x="206" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="221.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="16" y="124" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">k = 2，算 f[5] 时队列 = [3, 4]</text>
<text x="16" y="142" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">队首 f[3] = 4 最大：f[5] = 4 + 3 = 7</text>
</svg>

```python
def max_result(nums, k):
    n = len(nums)
    f = [0] * n
    f[0] = nums[0]
    q = deque([0])             # 下标，f 值从队首到队尾递减
    for i in range(1, n):
        if q[0] < i - k:
            q.popleft()        # 队首跳不到 i 了
        f[i] = f[q[0]] + nums[i]
        while q and f[q[-1]] <= f[i]:
            q.pop()            # 又旧又小，再也用不上
        q.append(i)
    return f[-1]
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 当成跳跃游戏贪心「跳到最大的数」：负数也可能必须踩，局部最优不对。
- 先入队再算 `f[i]`：会用 `f[i]` 自己去更新自己。

**追问。**
- 用堆可以吗？：最大堆存 `(f, 下标)`，堆顶过期就弹，`O(n log n)`。
- 为什么能弹掉队尾？：它比 `i` 更早过期且 `f` 不大于 `f[i]`，以后永远不会是最大值。

**同模式。** LC 239 滑动窗口最大值、LC 1425 带限制的子序列和、LC 862 和至少为 K 的最短子数组
