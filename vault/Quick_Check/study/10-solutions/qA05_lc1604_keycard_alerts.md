# qA05 · LC 1604 一小时内刷卡 ≥3 次告警

> `problems/qA05_lc1604_keycard_alerts/` · 3 个 part · LC Stripe tag 频率 62
> **主题：`HH:MM` → 分钟 + 窗口的闭合边界 + "被拒的不计数"。**

## 一句话题意

`key_name[i]` 在 `key_time[i]`（`HH:MM`）刷卡。
若某人在**任意一小时内刷了 ≥ 3 次**就告警。返回**排序去重**的名字列表。

## 直觉 / Intuition

- 把每个人的刷卡记录想成数轴上的一串点：一小时内 ≥3 次，等价于**存在长度为 3 的连续子序列，首尾间距 ≤60**。一旦想到"排序后只看相邻窗口"，就不需要真的维护滑动窗口、也不需要暴力两两比较时间差——`ts[i+2] - ts[i]` 直接把"任意一小时内 3 次"翻译成了固定跨度 3 的数组扫描。
- 这个 shape 之所以自然，是因为**告警条件与顺序无关，只与间距有关**：先排序把"任意一小时"这种模糊的时间窗口，转成了确定的相邻元素比较，问题从"区间计数"降级成了"定长窗口扫描"，复杂度直接从 O(n²) 降到 O(n log n)。
- Part 2 把 3 和 60 抽成 `k` 和 `window`，本质没变——还是同一句话："排序后看第 `i` 到第 `i+k-1` 个之间隔多久"。
- Part 3 从"事后审计"变成"实时限流"，直觉上是同一把尺子换了个用法：审计是"回头看窗口里有没有超标"，限流是"来一个判一个，只是窗口里只能数**被放行**的那些"——一旦意识到"被拒的不算数"，就知道不能简单复用一个计数队列，而要单独维护"已放行"的时间列表。

## 解题思路

### Part 1

```python
def alert_names(key_name, key_time):
    by = defaultdict(list)
    for n, t in zip(key_name, key_time):
        h, m = map(int, t.split(":")); by[n].append(h * 60 + m)
    out = []
    for n, ts in by.items():
        ts.sort()
        if any(ts[i+2] - ts[i] <= 60 for i in range(len(ts) - 2)):   # ★ <= 非严格
            out.append(n)
    return sorted(out)
```

**排好序之后只需要看 `ts[i+2] - ts[i]`** —— 不需要真的滑窗。

### Part 2 — 通用阈值

`alert_names_k(key_name, key_time, k=3, window=60)`：某个 `i` 满足
`times[i+k-1] - times[i] <= window` 就告警。
`k = 1` 会告警所有出现过的名字（一次刷卡就是"任意窗口内 1 次"）；
`k <= 0` 或 `window < 0` → `ValueError`。

### Part 3 — 在线限流器

`KeyCardLimiter(limit=2, window=60).swipe(name, time) -> bool`：
`[t - window, t]`（**两端闭**）内**已允许**的刷卡数 < `limit` 才允许。
**被拒的刷卡不计入后续窗口**（与 q23 同一条规则）。
每个名字的刷卡时间必须非递减，倒退则 `ValueError`。

`limit=2, window=60` 恰好拒掉那次会触发 LC 告警的刷卡。

## 坑

1. **窗口闭合**：恰好 60 分钟**告警**，61 不告警。
2. **没有跨午夜**：`23:30` 然后 `00:10` 是**倒退 20 分钟**，不是往后 40 分钟
   （这种输入按 Part 3 会 `ValueError`；Part 1 排序后差是 -1400，不会告警）。
3. **完全相同的时间（`10:40, 10:40`）算两次独立的刷卡。**
4. 每个名字的输入**未排序**；少于 3 次的名字**永远不会告警**；结果要**去重 + 排序**。
5. `HH:MM` 是**补零**的（`09:05`）；输出名字按**普通字符串序**。
6. Part 3：**被拒的不计数**；边界 `t - window` **在窗口内**；乱序 → 报错。

## 变体

- q23 限流器（每客户 5 次 / 2 秒；滑窗、带权、令牌桶）。
- qA04（窗口内的**异城**对，而不是计数）。
- 返回每个人的**首次告警时间**而不是名字列表。

## Code Core 节点

**`chrono.windows`** · **`chrono.parsing`**（`HH:MM` → 分钟） · `algorithms.sliding-window` ·
`rules.grouping` · `rules.thresholds` · `output.ordering`

## 自测清单

- [ ] 恰好 60 / 61 分钟
- [ ] `23:30` + `00:10`
- [ ] 相同时间两次
- [ ] 输入未排序；少于 3 次的名字
- [ ] 结果去重 + 排序
- [ ] `k = 1` / `k <= 0` / `window < 0`
- [ ] Part 3：被拒不计数、`t - window` 边界、时间倒退
