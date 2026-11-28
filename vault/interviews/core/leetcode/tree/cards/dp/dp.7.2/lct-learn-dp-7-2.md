---
id: lct-learn-dp-7-2
node: dp.7.2
type: qa
step: 1
---
## Q
**动态规划 › 其他线性 DP › 不相交区间**｜学习卡

套路是什么？

## A
**一句话。** 不相交区间 DP：按结束时间排序，`f[i+1]` 取「不做第 `i` 份」与「做第 `i` 份，接在最后一个能相容的前缀后」的较大值，用二分找前缀。

下图：做第 `i` 份时，只能接在「结束不晚于它开始」的那些工作之后，它们恰好是一个前缀。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<rect x="30" y="20" width="84" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="24" y="33" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="86" y="46" width="56" height="18" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80" y="59" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="58" y="72" width="112" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="52" y="85" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="142" y="98" width="112" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="136" y="111" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<line x1="142" y1="14" x2="142" y2="130" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<text x="146" y="138" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">s = 4</text>
<text x="264" y="98" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">job i</text>
<line x1="30" y1="130" x2="310" y2="130" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="20" y="156" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">按结束时间排序；结束 ≤ s 的有 k = 2 份（二分）</text>
<text x="20" y="172" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[i+1] = max(f[i], f[k] + p)：不做 / 做</text>
</svg>

```python
def job_scheduling(start, end, profit):
    jobs = sorted(zip(end, start, profit))   # 按结束时间排
    ends = [e for e, _, _ in jobs]
    f = [0] * (len(jobs) + 1)    # f[i]：前 i 份最优
    for i, (e, s, p) in enumerate(jobs):
        k = bisect_right(ends, s, 0, i)      # 结束 <= s 有 k 份
        f[i + 1] = max(f[i], f[k] + p)       # 不做 / 做
    return f[-1]
```

**要点。**
- 为什么对？：按结束时间排序后，与第 `i` 份不冲突的工作恰好是一个前缀，二分找到它的长度 `k`，`f[k]` 就是前面的最优。
- 首尾相接算冲突吗？：题目允许相接，所以用 `bisect_right`：结束时间等于 `s` 的也算进前缀。
- 没有报酬、只数个数怎么办？：就是区间调度，直接贪心（LC 435）；要限制最多做 `k` 份（LC 1751）则 `f` 加一维。

**易错点。**
- 用 `bisect_left`：`[1,3]` 与 `[3,6]` 相接也兼容，会被漏掉。
- 按开始时间排序：可接的工作不再是前缀，`f[k]` 失效。
- `f[i + 1]` 不与 `f[i]` 取大：不做这份可能更优，`f` 必须单调不减。

**对应题目。** LC 1235 规划兼职工作
