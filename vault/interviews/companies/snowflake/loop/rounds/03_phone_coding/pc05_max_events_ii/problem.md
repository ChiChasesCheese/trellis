# pc05 · Max Events II — 至多参加 k 个不重叠活动的最大价值（LC 1751 + 两个追问）

> 40 分钟电面题。Part 1 是一手报道的原题；Part 2、Part 3 是这类题最常见的两个 follow-up（输出方案 / 去掉 k 限制放大规模），**(reconstructed)**。

## 背景

2026-06 一位 Snowflake SDE 候选人的技术电面：约 10 分钟介绍，40 分钟一道题——**LeetCode 1751 Maximum Number of Events That Can Be Attended II 的变体，外加 follow-up**，10 分钟反问。原帖正文在 1point3acres 付费墙后，只能确认题号、时长与"有 follow-up"。

这类题的真实难点不在"想到 DP"，而在三件事：**闭区间的重叠判定**、**找下一个可参加活动的二分**、**被追问"具体选了哪些"时能不重写**。

## 输入

每个活动是 `[start, end, value]`：
- `1 ≤ start ≤ end ≤ 10^9`，**end 是闭区间**——`[1,2]` 和 `[2,3]` 在第 2 天冲突，不能都参加；
- `value ≥ 0`；
- 同一时间只能参加一个活动，参加就要从 start 待到 end。

`start > end` 或 `value < 0` 视为非法输入，抛 `ValueError`。

## API 契约（英文签名）

```python
def max_value(events: list[list[int]], k: int) -> int
def max_value_with_events(events: list[list[int]], k: int) -> tuple[int, list[int]]
def max_value_unbounded(events: list[list[int]]) -> int
```

## 规则

### Part 1 — 至多 k 个（LC 1751 原题）

返回至多参加 `k` 个互不重叠活动能拿到的最大价值和。约束：`1 ≤ k·n ≤ 10^6`。`k = 0` 或没有活动 → `0`。

### Part 2 — 说出选了哪些 **(reconstructed)**

返回 `(最大价值, 选中活动的原始下标升序列表)`。可能有多种最优方案，**任意一种合法的最优方案都算对**：数量 ≤ k、两两不重叠、价值和等于最大值、下标升序无重复。（参考解在"选与不选价值相同"时优先选，所以样例输出是确定的。）

### Part 3 — 去掉 k 的限制，n 到 10^5 **(reconstructed)**

参加多少个都行，返回最大价值和。`n ≤ 10^5`，要求 2 秒内。**Part 1 的 `O(n·k)` 表在 `k = n` 时是 `10^10`，必须换思路。**

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1**（LC 官方例 1）
```
events = [[1,2,4],[3,4,3],[2,3,1]], k = 2
max_value → 7                  # 选 [1,2,4] 和 [3,4,3]
max_value_with_events → (7, [0, 1])
```

**例 2**（LC 官方例 2）
```
events = [[1,2,4],[3,4,3],[2,3,10]], k = 2
max_value → 10                 # [2,3,10] 和另外两个都冲突，只选它
max_value_with_events → (10, [2])
```

**例 3**（LC 官方例 3：k 限制生效）
```
events = [[1,1,1],[2,2,2],[3,3,3],[4,4,4]], k = 3
max_value → 9                  # 选价值最大的三个
max_value_with_events → (9, [1, 2, 3])
max_value_unbounded → 10       # 不限个数，四个全选
```

**例 4**（同一区间出现两次）
```
events = [[1,5,3],[1,5,1],[6,6,5]], k = 2
max_value → 8                  # [1,5,3] + [6,6,5]
```

## `main()` 命令流

```
PART 1            PART 2            PART 3
K 2               K 3               N 4
N 3               N 4               1 1 1
1 2 4             1 1 1             2 2 2
3 4 3             2 2 2             3 3 3
2 3 1             3 3 3             4 4 4
                  4 4 4
→ 7               → 9               → 10
                    1 2 3
```
Part 2 没有选中任何活动时第二行输出 `-`。

## 边界清单

- 相邻闭区间 `[1,2]`、`[2,3]` 冲突（最常见的 off-by-one）
- `k = 0`、空列表、`k > n`
- 单日活动 `[5,5,v]` 多个同一天
- 完全相同的区间出现多次
- 价值为 0 的活动（Part 2 不必把它放进方案）
- `start > end` / 负价值 → `ValueError`
- Part 1 `k·n = 10^6`（如 n = 2·10^4、k = 50）要在时限内
- Part 3 `n = 10^5`、坐标到 `10^9`

## 追问

1. **为什么按开始时间排序后二分找"下一个"，而不是按结束时间？** 两种都行：按 start 排序做"从 i 往后"的 DP，下一个是第一个 `start > end_i`；按 end 排序做"到 i 为止"的 DP，前驱是最后一个 `end < start_i`。Part 3 用后者更自然。
2. **内存能不能压到 O(n)？** Part 1 只需要相邻两层，可以；但 Part 2 要回溯方案，需要保留整张表或额外记录选择。
3. **如果活动是半开区间 `[start, end)`？** 二分从 `bisect_right(starts, end)` 改成 `bisect_left(starts, end)`。
4. **k 很大但 n 小？** `k` 截到 `min(k, n)`。
5. **流式输入、活动不断到来？** 按结束时间有序到达时 Part 3 的递推可以在线做；乱序到达需要平衡树维护前缀最大值。

## 来源与置信度

- **HIGH（题号 + 轮次 + 时长）**：1point3acres thread-1179486（2026-06，SDE 电面，"~10 min intros, 40 min coding with follow-ups, 10 min Q&A"，LC 1751 变体），经 Telegram 镜像 t.me/s/usinterview/28733 读到摘要。见 `../../../../raw/process_research.md` §3.2 #1 与 `../../../../catalog/CATALOG.md` Table A pc05。
- 原帖正文不可读，**follow-up 的具体内容未知**；Part 2 / Part 3 是按 LC 1751 同族题最常见的追问方向重建。
- LC 1751 官方题面：https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended-ii/

## 考什么

S03 加权区间调度 / 排序 + 二分 + DP · S08 在被追问时把复杂度压一档（k 维 DP → O(n log n)）· 闭区间边界的严谨性。
