---
id: lct-learn-data-structures-5-4
node: data-structures.5.4
type: qa
step: 1
---
## Q
**常用数据结构 › 堆（优先队列） › 重排元素**｜学习卡

套路是什么？

## A
**一句话。** 重排题的约束只和各字符剩余次数有关：每个位置放「剩余次数最多且已冷却」的字符，最大堆管次数，等待队列把刚用过的字符挡 `k` 个位置，堆空即无解。

下图：字符在堆、结果、等待队列之间循环；刚用过的字符要在队列里挡 `k` 个位置。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="19.0" y="20.0" width="112" height="40" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="75" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最大堆</text>
<text x="75" y="51.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">剩余次数多的在顶</text>
<rect x="220.6" y="27.5" width="88.7" height="25" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="265" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">放到 res[i]</text>
<rect x="101.6" y="110.0" width="136.7" height="40" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="126.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等待队列</text>
<text x="170" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">冷却到 i + k 才解冻</text>
<path d="M 131.0 40.0 L 220.6 40.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="220.6,40.0 214.3,43.0 214.3,37.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178" y="32" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">弹次数最多的</text>
<path d="M 265.0 52.5 L 265.0 130.0 L 238.4 130.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="238.4,130.0 244.7,127.0 244.7,133.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="292" y="95" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">还有剩余</text>
<path d="M 101.6 130.0 L 75.0 130.0 L 75.0 60.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="75.0,60.0 78.0,66.3 72.0,66.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="48" y="95" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">解冻位置 ≤ i</text>
<text x="170" y="180" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">某一步堆空（全在冷却）：无解，返回 ""</text>
</svg>

```python
def rearrange(s, k):                 # LC 358；LC 767 即 k = 2
    if k <= 1:
        return s                     # 没有间隔限制
    h = [(-c, ch) for ch, c in Counter(s).items()]
    heapify(h)                       # 最大堆：次数多的在堆顶
    wait, res = deque(), []          # wait：(解冻位置, 负次数, 字符)
    for i in range(len(s)):
        while wait and wait[0][0] <= i:     # 冷却完毕，回到堆
            _, c, ch = wait.popleft()
            heappush(h, (c, ch))
        if not h:                    # 没有可放的字符：无解
            return ""
        c, ch = heappop(h)
        res.append(ch)
        if c + 1 < 0:                # 还有剩余：冷却 k 个位置
            wait.append((i + k, c + 1, ch))
    return "".join(res)
```

**要点。**
- 为什么贪心取最多？：最多者最容易成为瓶颈，它可用却放了次数少的，只会让局面更紧（交换论证）；最多者出现 `mx` 次至少占 `(mx - 1) * k + 1` 个位置，位置不够就无解，表现为堆空。
- LC 621 怎么改？：只问时间，不必建堆，次数最多的任务撑起骨架：`max(len(tasks), (mx - 1) * (n + 1) + num)`，`num` 是并列最多的种数。
- LC 1405 怎么改？：约束变成「至多连续两个」，不用冷却队列；连放了两个同字符时改放次多的垫一个，且最多者要立刻放回堆。

**易错点。**
- 解冻位置写成 `i + 1`：`"aab"`、`k = 2` 应得 `"aba"`，错写会得 `"aab"`。
- 堆空时直接 `heappop`：`"aaab"` 无解，应返回 `""`。
- LC 621 漏掉并列个数 `num`：`["A","A","A","B","B","B"]`、`n = 2` 应得 `8`；漏掉 `len(tasks)` 的比较：`["A","A","B","B"]`、`n = 0` 应得 `4`。

**对应题目。** LC 1405 最长快乐字符串、LC 358 K 距离间隔重排字符串、LC 767 重构字符串、LC 621 任务调度器
