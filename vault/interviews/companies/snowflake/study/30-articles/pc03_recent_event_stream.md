# pc03 · Recent Event Stream：练的是"deque 管窗口，计数哈希管查询"

> [!tldr]
> - Part 1 按条数保留最近 m 条（fastprep + prachub 两个来源，例子 `m=3 → ["2","a","2","a"]`）；**Part 2 按时间窗口保留是 (reconstructed)**
> - 这题考的是：流式事件的滑动窗口，支持"窗口内严格早于 ts 的不同 key 数"与"窗口内最频繁的 key"
> - 三步套路：deque 存 `(ts, key)` → Counter 跟着进出窗口增减 → 出窗时计数归零要删 key
> - 最值得带走的一个模式：**窗口的"进"和"出"是对称的两段代码**，计数的增减必须成对出现；只写"进"不写"出"是这类题最常见的 bug

## 1. 题目在说什么（人话版）

事件一条条来（时间戳不递减），系统只记最近的一部分。随时可能被问两件事：窗口里时间戳严格早于某个值的事件涉及多少个**不同** key；窗口里哪个 key 出现最多（并列取字典序最小）。Part 1 的"最近"是最近 m 条；Part 2 的"最近"是最近 W 秒。

小例子（Part 1，m=3）：
```
record 1 a, record 2 b, record 3 a   窗口 [a b a]
count 10 → 2（a、b）   top → a
record 4 a                          窗口 [b a a]（第一条 a 被挤出）
count 10 → 2           top → a
```

## 2. 读题：把文字变成模型

- **实体**：事件 `(ts, key)`、窗口、查询。
- **输出**：每个 COUNT / TOP 一行；RECORD 不输出。
- **状态**：`deque[(ts, key)]` 窗口、`Counter[key]` 窗口内计数。
- **一句话建模**：这是一个 **"按条数或按时间出窗的滑动窗口 + 窗口内频次统计"** 问题。

> [!note] 为什么不每次查询重扫全部历史
> 流可以无限长，窗口有上界（m 或 W 秒内的事件）。只维护窗口内的数据，查询代价与窗口大小相关而不是与历史长度相关。

## 3. 下笔顺序

1. **问清**：`count` 是"不同 key 数"还是"事件条数"？"严格早于"还是"不晚于"？空窗口 `top` 返回什么？时间戳是否单调？
2. **Part 1 record**：append → 计数加一 → 超过 m 就 popleft 并计数减一，归零删 key。
3. **Part 1 查询**：`count(ts)` 扫窗口收集 `t < ts` 的 key；`top` 在 Counter 里找最大计数，再在并列里取最小 key。
4. **Part 2**：record 时**先**把 `t <= ts - W` 的事件出窗，**再** append（窗口为 0 秒时新事件不能把自己踢掉）。查询完全复用。
5. **收尾**：空窗口、`count` 边界（ts 等于某事件时间戳）、并列取字典序。

## 4. 代码怎么组织

```
RecentEventStream(m)                  # Part 1：record / count / top
RecentEventStreamByTime(W)            # Part 2：只有 record 的出窗条件不同
process_recent_event_stream(ops, m)   # 操作列表驱动，测试共用一种形状
_parse_ops / part1 / part2            # 命令流
```
两个类的 `count`/`top` 完全一样，差别只在 record 的出窗条件——面试里可以提"抽一个基类，出窗策略作为钩子"。

## 5. 核心代码骨架

```python
class RecentEventStream:
    def __init__(self, m):
        self.m, self.win, self.cnt = m, deque(), Counter()

    def _evict_one(self):
        _, k = self.win.popleft()
        self.cnt[k] -= 1
        if self.cnt[k] == 0:
            del self.cnt[k]                      # 归零必须删，否则 top 会看到计数 0 的 key

    def record(self, ts, key):
        self.win.append((ts, key)); self.cnt[key] += 1
        if len(self.win) > self.m:
            self._evict_one()

    def count(self, ts):
        return len({k for t, k in self.win if t < ts})

    def top(self):
        if not self.cnt:
            return ""
        best = max(self.cnt.values())
        return min(k for k, c in self.cnt.items() if c == best)

class RecentEventStreamByTime(RecentEventStream):
    def record(self, ts, key):                   # 先出窗，再入窗
        while self.win and self.win[0][0] <= ts - self.window_seconds:
            self._evict_one()
        self.win.append((ts, key)); self.cnt[key] += 1
```

## 6. 每个 part 叠加什么

| Part | 窗口定义 | 改动 |
|---|---|---|
| 1 | 最近 m 条 | append 后超 m 就出窗 |
| 2 | `(最新 ts − W, 最新 ts]` | append 前按时间出窗 |

## 7. 常见坑

- 出窗时忘了计数减一，或减到 0 没删 key（`top` 返回一个窗口里已经没有的 key）。
- `count` 返回事件条数而不是不同 key 数。
- 严格早于 vs 不晚于。
- Part 2 先 append 再出窗：W = 0 时新事件把自己踢掉。
- `top` 并列时取了计数最大里"最先出现"的而不是字典序最小的。

## 8. 追问怎么接

1. **`top` 在 key 很多时太慢？** 维护"计数 → key 集合"的桶加当前最大计数指针（LFU 同款），入窗 +1、出窗 −1 都 O(1)；字典序 tie 在桶内用有序结构。
2. **`count(ts)` 每次扫窗口太慢？** 窗口按时间有序，二分找到 `ts` 的位置；不同 key 数需要"每个 key 在窗口内最早出现位置"的辅助结构。
3. **事件乱序到达？** 设允许的延迟上界，用最小堆按时间暂存，超过水位线才放进窗口（流处理里的 watermark）。
4. **分布式、多分区？** 每分区一个窗口，查询时合并计数；top-k 用近似结构（Count-Min Sketch + 堆）。

## 9. 自测清单

- [ ] 写出成对的"入窗计数 +1 / 出窗计数 −1 并删零"
- [ ] 说清 Part 2 为什么先出窗再入窗
- [ ] 口述 O(1) top 的桶结构

## 相关题与 skills

S06 滑窗与事件流。相关：`od04` 限流器（同一半开窗口写法）、`od08` LRU/TTL、Stripe `ps01` / `cd06`（同族滑窗）。
