# pc26 · Top K Hashtags：练的是"去重计数必须维护集合 + 滑动窗口用闭区间处理退化情形"

> [!tldr]
> - 这题考的是：热度 = 发过该 tag 的去重用户数（不是事件总数），从全量排名到流式类再到滑动时间窗；Part 1 一手预览原题，流式类与滑动窗口 **(reconstructed)**
> - 三步套路：按 tag 分组存 `set[user]` → 排序键 `(-热度, tag)` 取前 k → 滑动窗口用闭区间 `[max_ts-W, max_ts]` 处理 `W=0` 的退化情形
> - 最值得带走的一个模式：**去重计数必须维护成员关系（集合），不能只用计数器增量维护；滑动窗口的边界要用闭区间处理"窗口为 0"这类退化情况**

## 1. 题目在说什么（人话版）

`events = [(user, tag), ...]`，每个 tag 的热度是**发过它的去重用户数**（同一个用户反复发同一
个 tag 只算一次），按热度降序、tag 字典序升序取前 k。Part 2 把它变成一个流式类（`add`/`top`
频繁调用）；Part 3 加上滑动时间窗，只统计"最近 `window_seconds` 秒"内的事件。

小例子：
```python
events = [("u1","snow"),("u2","snow"),("u1","cloud"),("u3","snow"),("u2","cloud"),("u4","data")]
top_k_hashtags(events, 2) -> [("snow", 3), ("cloud", 2)]
top_k_hashtags([("u1","a"),("u1","a"),("u1","a")], 5) -> [("a", 1)]   # 同一用户重复发只算一次
```

## 2. 读题：把文字变成模型

- **实体**：用户、tag、`(user, tag)` 事件（Part 3 多一个时间戳）。
- **输入**：Part 1/3 是事件列表 + k（+窗口秒数）；Part 2 是增量的 `add`/`top` 调用。
- **输出**：`(tag, 去重用户数)` 列表，按热度降序、tag 升序，取前 k。
- **状态**：`dict[tag -> set[user]]`——这是任何正确实现都绕不开的最小状态。
- **一句话建模**：这是一个 **"分组去重计数 + 确定性排序 tie-break"** 问题；Part 3 的窗口是相对
  于"事件里最大的时间戳"而不是"现在"。

> [!note] 为什么必须维护 `set[user]`，不能只用一个计数器
> "某 tag 的去重用户数"不能靠一个数字做增量维护——同一用户重复发同一个 tag 不能让计数器涨。
> 必须能判断"这个用户是不是已经算过这个 tag 了"，所以状态至少是 `dict[tag -> set[user]]`，这是
> 天真实现最容易被同一用户刷屏的数据戳穿的地方。

## 3. 下笔顺序

1. **问清**：热度打平时按什么排序？`k` 大于种类数怎么办？
2. **Part 1 最小可用**：按 tag 分组，组内放 `set[user]`；排序键 `(-len(set), tag)`；切片前 k。
3. **Part 2 叠加**：把同样的 `dict[tag -> set[user]]` 包进一个类，`add` 只做集合插入，`top(k)`
   每次对全部 tag 重新排序（诚实说明这是 `O(T log T)`，不是渐进最优，真正最优需要按热度排序的
   平衡结构）。
4. **Part 3 叠加**：先扫描全部事件取 `max_ts`（不能假设输入按时间排序、更不能假设最后一条最新）
   ，用闭区间 `[max_ts - window_seconds, max_ts]` 过滤事件，其余逻辑复用 Part 1。
5. **收尾**：负数 `k`/`window_seconds` 报错；空结果输出用一个明确标记而不是空行；
   `window_seconds = 0` 要保留恰好等于 `max_ts` 的事件。

## 4. 代码怎么组织

```
top_k_hashtags(events, k)                    # Part 1：分组去重 + 排序取前 k
class HashtagCounter:
    add(user, tag)                           # Part 2：增量维护 set
    top(k)                                   # Part 2：全量重排序，口头讨论更优设计
top_k_hashtags_windowed(events, k, window)   # Part 3：先过滤窗口内事件，复用 Part 1 逻辑
```
三者共用同一个排序键 `(-len(users), tag)`；差别只在"哪些事件参与分组"。

## 5. 核心代码（骨架）

```python
def top_k_hashtags(events, k):
    if k < 0:
        raise ValueError("k must be >= 0")
    users_by_tag = defaultdict(set)
    for user, tag in events:
        users_by_tag[tag].add(user)
    ranked = sorted(users_by_tag.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return [(tag, len(users)) for tag, users in ranked[:k]]

class HashtagCounter:
    def __init__(self):
        self._users_by_tag = defaultdict(set)

    def add(self, user, tag):
        self._users_by_tag[tag].add(user)     # 天然去重，重复 add 不涨热度

    def top(self, k):                          # O(T log T)：每次重排序，非渐进最优
        ranked = sorted(self._users_by_tag.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        return [(tag, len(u)) for tag, u in ranked[:k]]

def top_k_hashtags_windowed(events, k, window_seconds):
    if not events:
        return []
    max_ts = max(ts for ts, _, _ in events)
    cutoff = max_ts - window_seconds            # 闭区间 [cutoff, max_ts]
    users_by_tag = defaultdict(set)
    for ts, user, tag in events:
        if ts >= cutoff:
            users_by_tag[tag].add(user)
    ranked = sorted(users_by_tag.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return [(tag, len(u)) for tag, u in ranked[:k]]
```

## 6. 面试里怎么说

- 开始前：「热度打平的时候按 tag 字典序升序，对吗？`k` 大于种类数就返回全部？」
- 写 Part 1 时：「我按 tag 分组存一个 `set[user]`，热度是集合大小，而不是事件条数——同一个用户
  刷屏不会让热度虚高。」
- 到 Part 2 的复杂度追问时：「我这版 `top(k)` 每次全量重排序是 `O(T log T)`，不是渐进最优；真正
  最优需要一个按热度排序的平衡结构，`add` 增量更新到 `O(log T)`，但实现和调试成本超出电面时间
  预算，我先讲清楚这个权衡。」
- 到 Part 3 时：「窗口是相对'所有事件里最大的时间戳'，不是'现在'，因为这是离线批量查询；我用
  闭区间 `[max_ts-W, max_ts]`，这样 `W=0` 时也能正确保留恰好等于 `max_ts` 的事件。」

## 7. 常见跑偏

- 直接用 `Counter((user, tag) for ...)` 数事件条数，被同一用户反复发同一 tag 的数据戳穿——这是
  这题最容易被抓到的地方。
- Part 3 假设输入按时间排序、或假设最后一条事件时间戳最大，没有显式扫描取 `max_ts`。
- Part 3 窗口用开区间 `ts > cutoff`，导致 `window_seconds = 0` 时把 `max_ts` 自己也排除掉，
  和"最近 0 秒也该看到刚发生的事件"的直觉矛盾。

## 8. 同族题 / 延伸

- 与 `pc03`（Recent Event Stream 的 `top` 查询）同属"计数 + 确定性排序 tie-break"的考法，pc03
  是滑动窗口内的实时 top，pc26 是离线批量或流式增量的 top-k。
- 与 `pc22`（Document Predicate Search）同样维护一个随增量更新的哈希结构，但 pc22 考集合代数
  与解析器，pc26 考去重计数与排序。
- 练习命令：`python3 loop/mock.py start pc26`

## 索引行

| [pc26_top_k_hashtags](pc26_top_k_hashtags.md) | `../../loop/rounds/03_phone_coding/pc26_top_k_hashtags/` | 电面 coding | 去重计数必须维护成员关系（集合），不能只用计数器增量维护；滑动窗口的边界要用闭区间处理"窗口为 0"这类退化情况 |
