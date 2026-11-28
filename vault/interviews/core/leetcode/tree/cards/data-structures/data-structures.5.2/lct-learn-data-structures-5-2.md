---
id: lct-learn-data-structures-5-2
node: data-structures.5.2
type: qa
step: 1
---
## Q
**常用数据结构 › 堆（优先队列） › 进阶**｜学习卡

套路是什么？

## A
**一句话。** 进阶堆题是「排序 + 扫描 + 堆 + 一个贪心理由」：按某个键排序，扫到哪就把「已有资格」的元素压进堆，从堆顶取最优，过期的等浮到堆顶再丢（懒删除）。

下图：排序 + 扫描 + 堆 + 懒删除的循环（以 LC 1353 为模板）；堆顶永远是已开始会议里结束最早的。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 275">
<rect x="106.0" y="7.5" width="88" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按开始日排序</text>
<polygon points="124.0,65.0 133.0,52.5 167.0,52.5 176.0,65.0 167.0,77.5 133.0,77.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="69.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆空？</text>
<rect x="236.0" y="45.0" width="88" height="40" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="280" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">day 跳到</text>
<text x="280" y="76.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下一场开始日</text>
<rect x="63.6" y="102.5" width="172.7" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">开始日 ≤ day 的结束日入堆</text>
<rect x="57.6" y="147.5" width="184.7" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="164.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">弹掉堆顶 &lt; day 的（懒删除）</text>
<rect x="66.2" y="192.5" width="167.7" height="25" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="150" y="209.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">堆非空：弹堆顶，ans += 1</text>
<rect x="114.2" y="237.5" width="71.7" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="254.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">day += 1</text>
<path d="M 150.0 32.5 L 150.0 52.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,52.5 147.0,46.2 153.0,46.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 176.0 65.0 L 236.0 65.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.0,65.0 229.7,68.0 229.7,62.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="210" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 150.0 77.5 L 150.0 102.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,102.5 147.0,96.2 153.0,96.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="158.0" y="94.0" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 280.0 85.0 L 280.0 115.0 L 236.4 115.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.4,115.0 242.7,112.0 242.7,118.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 150.0 127.5 L 150.0 147.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,147.5 147.0,141.2 153.0,141.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 150.0 172.5 L 150.0 192.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,192.5 147.0,186.2 153.0,186.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 150.0 217.5 L 150.0 237.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,237.5 147.0,231.2 153.0,231.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 114.2 250.0 L 20.0 250.0 L 20.0 65.0 L 124.0 65.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="124.0,65.0 117.7,68.0 117.7,62.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>

```python
def max_events(events):              # LC 1353
    events.sort()                    # 按开始日排序
    h, i, day, ans = [], 0, 0, 0     # h：已开始会议的结束日
    while i < len(events) or h:
        if not h:
            day = events[i][0]       # 堆空：跳到下一场开始那天
        while i < len(events) and events[i][0] <= day:
            heappush(h, events[i][1])    # 今天可参加的入堆
            i += 1
        while h and h[0] < day:
            heappop(h)               # 已结束：懒删除
        if h:
            heappop(h)               # 参加结束最早的那场
            ans += 1
        day += 1
    return ans
```

**要点。**
- 为什么对？：交换论证，名额给结束更晚的会议，换成结束更早的不会更差，所以每天参加「结束最早且未过期」的；排序加指针让每场只入堆一次，懒删除让它最多出堆一次，`O(n log n)`。
- 枚举 + 保留前 `k`（LC 1383、LC 857）怎么做？：按维度 A 排序，依次枚举「当前瓶颈」，把维度 B 压入最多 `k` 个的堆，超员弹掉最差的，每步用堆内总和更新答案；1383 按效率降序、小根堆存速度；857 按工资质量比升序、大根堆存质量，堆满 `k` 人才算成本。
- 扩展型（LC 23、LC 407）怎么做？：堆里放 `(代价, 位置)`，弹出最小的再沿后继扩展，弹出时代价已定；23 放各链表队头；407 从外圈开始，水位 `max(w, 格高)`，低于水位的格子存水。
- LC 502、LC 1851、LC 2402 怎么改？：502 项目按资本排序，资本够的利润入大根堆，取 `k` 次最大；1851 查询从小到大处理，左端点已到的区间按 `(长度, 右端点)` 入堆，右端点过期则丢；2402 空闲房间堆加占用房间堆 `(结束时间, 房间号)`，没空房就延后到最早结束的房间。

**易错点。**
- LC 1353 不丢过期会议：`[[1,1],[1,1]]` 应得 `1`，漏掉 `h[0] < day` 会得 `2`。
- LC 1383 直接取速度最大的 `k` 个：`speed = [2,10,3,1,5,8]`、`eff = [5,4,3,9,7,2]`、`k = 2` 应得 `60`，不是 `36`；要枚举最低效率，且最后才取模。
- LC 407 入堆的键写成格子高度而不是水位 `max(w, 高度)`：`[[5,5,5,5],[5,1,2,5],[5,5,5,5]]` 应得 `7`，写成格高会得 `4`。

**对应题目。** LC 23 合并 K 个升序链表、LC 2402 会议室 III、LC 1353 最多可以参加的会议数目、LC 1383 最大的团队表现值、LC 407 接雨水 II、LC 502 IPO（IPO）、LC 857 雇佣 K 名工人的最低成本、LC 1851 包含每个查询的最小区间（Minimum Interval to Include Each Query）
