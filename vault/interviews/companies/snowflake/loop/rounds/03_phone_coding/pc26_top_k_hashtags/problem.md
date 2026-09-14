# pc26 · Top K Hashtags — 去重用户数的热度排名 + 流式类 + 滑动时间窗

> 一手预览只给出 Part 1 的原题面；流式类与滑动窗口均超出预览，**(reconstructed)**。

## 背景

TrueInterview 题单预览：`events = [userId, hashtag]`，热度 = **发过该 tag 的去重用户数**（不是
事件总数——同一个用户反复发同一个 tag 只算一次），按热度降序、tag 字典序升序取前 k。这题的坑就
在"去重"两个字：一个天真实现直接数 `(user, tag)` 事件条数会在测试里被同一用户刷屏的数据戳穿。

## 输入

- Part 1：`events: list[tuple[str, str]]`（`(user_id, hashtag)`）、`k: int >= 0`。
- Part 2：一个类，`add(user, tag)` 增量写入，`top(k)` 频繁查询当前快照。
- Part 3：`events: list[tuple[int, str, str]]`（`(timestamp, user_id, hashtag)`，**不保证按时
  间排序**）、`k: int >= 0`、`window_seconds: int >= 0`；只统计"最近 `window_seconds` 秒"内的事
  件（相对于所有事件里**最大的时间戳**，含端点）。

## API 契约（英文签名）

```python
def top_k_hashtags(events: list[tuple[str, str]], k: int) -> list[tuple[str, int]]

class HashtagCounter:
    def add(self, user: str, tag: str) -> None
    def top(self, k: int) -> list[tuple[str, int]]

def top_k_hashtags_windowed(
    events: list[tuple[int, str, str]], k: int, window_seconds: int
) -> list[tuple[str, int]]
```

`k < 0` 或 `window_seconds < 0` → `ValueError`。

## 规则

### Part 1 — 全量去重排名（原题）

按 tag 分组，组内放一个 `set[user]`；热度 = `len(set)`；排序键 `(-热度, tag)`；取前 `k` 个，
`k` 大于种类数时返回全部。

### Part 2 — 流式类，`top(k)` 高频调用 **(reconstructed)**

维护 `dict[tag -> set[user]]`：这是**任何正确实现都绕不开的最小状态**——"某 tag 的去重用户数"
不能只靠一个计数器算增量维护（同一用户重复 `add` 同一个 tag 不能让计数器涨），必须能判断"这个
用户是不是已经算过这个 tag 了"。

**`top(k)` 的复杂度诚实讨论**：本实现每次 `top(k)` 都对全部 tag 重新排序，`O(T log T)`
（`T` = 已出现的不同 tag 数）。这**不是**渐进最优的设计——真正的最优做法是维护一个按
`(热度, tag)` 排序的平衡结构（比如按热度分桶的 Fenwick 树，或跳表），每次 `add` 增量更新到
`O(log T)`，`top(k)` 做到 `O(k + log T)`；面试时间通常不够从零写一棵这样的结构，本题的测试规模
也不会暴露两者的差距，追问里口头说明这个更优设计即可（见"追问"）。

### Part 3 — 滑动时间窗 **(reconstructed)**

窗口是"最近 `window_seconds` 秒"，**相对于所有事件里最大的时间戳** `max_ts`（不是相对于"现
在"，因为这是一个离线批量查询，没有"现在"这个概念），是一个**闭区间**
`[max_ts - window_seconds, max_ts]`：即只统计 `ts >= max_ts - window_seconds` 的事件。
`window_seconds = 0` 时闭区间退化成单点 `{max_ts}`，正好只留下时间戳等于 `max_ts` 的事件——这也
是选闭区间而不是"`ts > cutoff`"的原因：后者会在 `window_seconds = 0` 时把 `max_ts` 自己也排除
掉，明显不符合"最近 0 秒也该看到刚刚发生的事件"的直觉。**同一个用户在窗口内对同一个 tag 只算一
次**，即使他在窗口内发了好几次。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1**（Part 1，基本去重排名）
```python
events = [("u1","snow"), ("u2","snow"), ("u1","cloud"), ("u3","snow"), ("u2","cloud"), ("u4","data")]
top_k_hashtags(events, 2) -> [("snow", 3), ("cloud", 2)]
```

**例 2**（Part 1，同一用户重复发同一 tag 只算一次）
```python
top_k_hashtags([("u1","a"), ("u1","a"), ("u1","a")], 5) -> [("a", 1)]
```

**例 3**（Part 2，流式增量）
```python
c = HashtagCounter()
c.add("u1", "snow"); c.top(2) -> [("snow", 1)]
c.add("u2", "snow"); c.top(2) -> [("snow", 2)]
c.add("u1", "cloud"); c.top(2) -> [("snow", 2), ("cloud", 1)]
```

**例 4**（Part 3，滑动窗口）
```python
events = [(1,"u1","snow"), (2,"u2","snow"), (100,"u3","snow"),
          (101,"u1","cloud"), (102,"u4","cloud"), (103,"u5","cloud")]
# max_ts = 103
top_k_hashtags_windowed(events, 2, 10)   -> [("cloud", 3), ("snow", 1)]   # cutoff=93，只留 ts>93
top_k_hashtags_windowed(events, 2, 1000) -> [("cloud", 3), ("snow", 3)]   # 全窗口，打平按 tag 升序
```

## `main()` 命令流

```
PART 1                          PART 2                       PART 3
N 6                             N 5                           N 6
u1,snow                         ADD u1,snow                   1,u1,snow
u2,snow                         TOP 2                         2,u2,snow
u1,cloud                        ADD u2,snow                   100,u3,snow
u3,snow                         TOP 2                         101,u1,cloud
u2,cloud                        ADD u1,cloud                  102,u4,cloud
u4,data                         → Q 1                         103,u5,cloud
K 2                                snow 1                     K 2 W 10
→ snow 3                          Q 1                         → cloud 3
  cloud 2                           snow 2                      snow 1
```

Part 1/2/3 都在没有任何结果时输出一行 `-`。

## 边界清单

- 同一用户重复发同一 tag（去重，见例 2）
- 热度打平按 tag 字典序升序（见例 4 的 `window=1000` 情形）
- `k = 0`、`k` 大于 tag 种类数
- 空 `events` → 空结果
- Part 2 从未调用 `top()` → 输出 `-`
- Part 3 `events` 不按时间排序（`max_ts` 要扫描全体取最大值，不能假设最后一条最新）
- Part 3 `window_seconds` 覆盖到全部事件、只覆盖最后一条事件、`window_seconds = 0`（只留
  `ts == max_ts` 的事件）
- 负数 `k` / `window_seconds` → `ValueError`

## 追问

1. **Part 2 的 `top(k)` 能不能做到 `O(k + log T)`？** 需要一个按热度排序的结构（比如"热度桶"数
   组 + 每个桶内一个 tag 集合，`add` 让某 tag 的热度从 `c` 变 `c+1` 就是把它从桶 `c` 移到桶
   `c+1`，`O(1)` 摊还），`top(k)` 从最高热度桶往下扫，桶内按 tag 排序取够 `k` 个为止；实现复杂
   度和调试成本远高于面试时间预算，属于"知道怎么做但不当场写"的追问。
2. **Part 3 如果窗口是"相对当前时间"而不是"相对最大时间戳"？** 那需要一个外部的"当前时间"输
   入（离线批量测试没有这个概念），逻辑不变，只是 `cutoff = now - window_seconds`。
3. **Part 3 要支持增量流式（新事件不断到达，窗口跟着往前移）吗？** 那是 Part 2 和 Part 3 的合
   并：用一个按时间排序的 deque 维护窗口内事件，过期事件从左边弹出时要相应地把该用户从对应 tag
   的 `set` 里移除——但"移除"要小心同一用户对同一 tag 在窗口内如果还有更新的事件，不能真的移除，
   这是滑动窗口 + 去重计数结合时最容易出 bug 的地方，本题不要求实现，只要求口头说清楚这个坑。
4. **热度定义换成"事件总数"而不是"去重用户数"？** 那是纯粹的计数问题，`Counter` 一行搞定；本题
   故意选"去重用户数"就是要考察这个区别。

## 来源与置信度

- **MED**：TrueInterview 同步的 Snowflake Algo 87 题清单第 26 项「Top K Hash Tags」，经
  `kevin-2023-code/Tech-Interview-Questions`（聚合站，题面付费，仅预览的一句原题面可见），见
  `../../../catalog/raw/github_repos.md` §2 第 26 行、§3 "pc26"。
- Part 2 的流式类、Part 3 的滑动时间窗均为重建，已标注 **(reconstructed)**；是聚合排名类题目最
  常见的两个追问方向（同族见本 kit `pc12`、`pc11`）。

## 考什么

S06（计数/聚合哈希 + 确定性排序 tie-break，与 pc11、pc12、pc03 同一类考法）· 去重 vs 计数的区
分（这题最容易被戳穿的地方）· 对"渐进最优但实现成本高"的设计能不能诚实讲清楚而不是假装写出来。
