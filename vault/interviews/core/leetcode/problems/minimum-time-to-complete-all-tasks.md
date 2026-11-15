---
slug: minimum-time-to-complete-all-tasks
---
## Q
**LC 2589 完成所有任务的最少时间**｜Hard

电脑可同时跑任意多个任务。任务 `[start, end, duration]` 需要在闭区间 `[start, end]` 内运行 `duration` 个整数时刻（可不连续）。求电脑最少开机多少秒（时刻 `<= 2000`）。

## A
**一句话。** 按结束时间排序；每个任务先复用区间内已开机的时刻，不够的部分从 `end` 往前找关机的时刻开，让开机时刻尽量靠后、被后面的任务共用。

**图解。** 任务按结束时间处理：`[1,3]` 开 2、3；`[2,5]` 已有 2 个，再开 5；`[5,6]` 已有 1 个，再开 6，共 4 秒。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 228">
<text x="83" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时刻</text>
<text x="106.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="136.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="166.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<text x="196.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<text x="226.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5</text>
<text x="256.0" y="30.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6</text>
<text x="83" y="64.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[1,3] 要 2</text>
<rect x="91" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="121" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="151" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="181" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="211" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="241" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="98.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[2,5] 要 3</text>
<rect x="91" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="121" y="80" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="151" y="80" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="181" y="80" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="211" y="80" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="241" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="132.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[5,6] 要 2</text>
<rect x="91" y="114" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="121" y="114" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="151" y="114" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="181" y="114" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="211" y="114" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="241" y="114" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="166.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">开机</text>
<rect x="91" y="148" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="121" y="148" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="151" y="148" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="181" y="148" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="211" y="148" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="241" y="148" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="16" y="192" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">浅色是任务区间，深色是开机时刻</text>
<text x="16" y="210" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor" font-weight="600">开机 2、3、5、6，共 4 秒</text>
</svg>

```python
def find_minimum_time(tasks):
    tasks.sort(key=lambda t: t[1])   # 按结束时间
    on = [False] * 2001        # 这一秒是否开机
    for s, e, d in tasks:
        d -= sum(on[s:e + 1])  # 已开的时刻直接复用
        t = e
        while d > 0:           # 从后往前补，留给后面的任务
            if not on[t]:
                on[t] = True
                d -= 1
            t -= 1
    return sum(on)
```

**复杂度。** 时间 `O(n·T)`（`T = 2000`），空间 `O(T)`。

**易错点。**
- 从 `start` 往后开：靠前的时刻对后面的任务没用，会多开。
- 复用后 `d` 变成负数还继续：`while d > 0` 自然跳过，不要写成 `!= 0`。

**追问。**
- 时刻到 `10^9`？：用线段树维护区间已开机数，并支持「从右往左把最靠右的若干个关机时刻打开」；或用单调栈存开机的连续段。
- 为什么按结束时间排序？：结束早的任务限制最紧，它的开机时刻放在自己区间的最右端，最可能被结束更晚的任务覆盖。

**同模式。** LC 452 用最少数量的箭引爆气球、LC 757 设置交集大小至少为2
