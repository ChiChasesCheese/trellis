---
id: uth-os-net-tcp-3-bbr
node: os-net.tcp
type: qa
step: 3
---
## Q
**BBR 不看丢包，看什么**｜Linux · tcp_bbr · 内核 7.3

CUBIC 靠丢包判断拥塞，BBR 靠什么调速度？

## A
**背景。** CUBIC 这类算法拿丢包当拥塞的信号，可丢包出现时路由器的队列早已塞满，延迟已经暴涨；有的丢包还只是线路噪声。BBR 换了问法：把网络想成一根水管，能装的量 = 带宽 × 往返时间；只要在途数据刚好装满水管，就既跑满带宽，又不排队。

**结构。** BBR 持续估计两个量：瓶颈带宽 = 最近 10 个往返里测到的最大交付速率（只看最近一段里的最大值，windowed max），最小 RTT = 最近 10 秒里的最小值。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 224">
<line x1="50" y1="18" x2="50" y2="90" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="50" y1="90" x2="322" y2="90" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="50" y1="118" x2="50" y2="190" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="50" y1="190" x2="322" y2="190" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">往返时间 RTT</text>
<text x="56" y="114" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">交付速率</text>
<polyline points="50,70 160,70 318,26" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<polyline points="50,188 160,138 318,138" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="160" y1="18" x2="160" y2="196" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="160" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">BDP 管道刚好装满</text>
<text x="60" y="60" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">最小 RTT</text>
<text x="250" y="132" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">瓶颈带宽</text>
<text x="322" y="212" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">在途数据</text>
</svg>
```

**细节。**

- 发送速率 = `pacing_gain` × 瓶颈带宽（`pacing_gain` 是发送速率相对于估计带宽的倍数）；`cwnd` = 2 × 带宽 × `min_rtt`
- 稳态循环：增益 5/4（多探测一点带宽）→ 3/4（排空刚多发的队列）→ 1.0 巡航
- 启动阶段增益取 2/ln2 ≈ 2.89，是让发送速率每个 RTT 翻倍的最小增益

**为什么。** 丢包不等于拥塞，而队列堆积会让延迟暴涨；直接建模“管道容量 = 带宽 × RTT”更稳。

**例题：** LC 239 滑动窗口最大值（同类：LC 862 和至少为 K 的最短子数组）

大小为 `k` 的窗口从数组最左侧每次右移一位，返回每个窗口位置上的最大值。例：`nums=[1,3,-1,-3,5,3,6,7]`，`k=3` → `[3,3,5,5,6,7]`。

```python
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    window: deque[int] = deque()       # 存下标；对应的值从队首到队尾严格递减
    ans: list[int] = []
    for i, x in enumerate(nums):
        while window and nums[window[-1]] <= x:
            window.pop()               # 比 x 小（或相等）且更靠左的数，永远没有机会当最大值
        window.append(i)
        if window[0] <= i - k:         # 队首已经滑出窗口
            window.popleft()
        if i >= k - 1:                 # 窗口满了才记录
            ans.append(nums[window[0]])
    return ans
```
