# pc14 · Meeting Rooms II（LC 253）— 最少会议室 + 分配房间号

> 2026 届 intern VO 技术面。Part 1 是一手报道的原题形态（未见具体例子，页面登录墙后只剩一句话摘要）；Part 2（具体分配房间号）、Part 3（房间有容量、会议有规模）是同类题最常见的两个追问，**(reconstructed)**。

## 背景

1point3acres 上一篇 "Snowflake 2026 Software Engineer Intern VO Interview Experience" 帖子被 WebFetch 摘要抓到一句话："a meeting room scheduling problem to find the minimum rooms required for overlapping requests"，正文在登录墙后没能进一步核实。对应 LC 253 Meeting Rooms II 题族。

真正的坑不是"要不要用堆"，而是：**区间是半开的**（`[start, end)`，一个会议 5 点结束、另一个 5 点开始不算冲突——这跟本 kit 里 pc05 的闭区间约定正好相反，务必分清）；**分配房间号时"最小空闲房间号优先"要写死成确定性规则**；以及追问里"房间带容量"这种资源类型化的调度本质上是 NP-hard 的匹配问题，贪心不保证最优。

## 输入

- Part 1/2：`intervals: list[list[int]]`，每项 `[start, end]`，**半开区间且必须 `start < end`**（正时长）：连续两个会议里，前一个的 `end` 等于后一个的 `start` 不算重叠。
- Part 3：`meetings: list[tuple[int, int, int]]`，每项 `(start, end, size)`；`capacities: list[int]`，固定房间列表，房间号是列表下标（0-based）。
- `start >= end`（非正时长）、`size <= 0`、`capacity < 0` → 抛 `ValueError`。

## API 契约（英文签名）

```python
def min_meeting_rooms(intervals: list[list[int]]) -> int
def assign_rooms(intervals: list[list[int]]) -> list[int]
def assign_rooms_with_capacity(
    meetings: list[tuple[int, int, int]], capacities: list[int]
) -> list[int | None]
```

## 规则

### Part 1 — 最少需要几间会议室（LC 253 原题）

标准双指针扫描：把开始时间和结束时间分别排序，`starts[i] < ends[j]` 就说明需要新开一间房，否则说明有房间空出来了。

### Part 2 — 具体分配到哪个房间号 **(reconstructed)**

按开始时间处理会议（开始时间相同按原始下标排序，保证确定性），维护"正在使用的房间"（按结束时间排序的最小堆）和"刚空出来的房间号"（另一个最小堆）；**总是优先复用编号最小的空闲房间**，没有空闲房间才启用一个新编号（从 0 开始递增）。返回值按**原始输入顺序**给出每个会议分到的房间号。

### Part 3 — 房间有容量，会议有规模 **(reconstructed)**

现在房间数量固定（`capacities`），每个房间有自己的容量；每个会议有自己的规模 `size`，只能用容量 `>= size` 的房间。**贪心规则**：按开始时间处理会议（同上原始下标 tie-break），在"此刻空闲且容量够用"的房间里选**容量最小的那个**（容量相同选房间号最小的）；分不到房间的会议在结果里是 `None`。

**这个贪心不保证全局最优**——"给每个会议在线分配一个满足容量的房间"等价于一种带类型的区间图着色/装箱问题，一般情况下是 NP-hard 的精确匹配问题；本题只承诺实现**这个写死的贪心规则**并且测试只验证"是否严格遵守了这条规则"，不验证"是不是全局房间使用最少的方案"。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1**（LC 官方例 1）
```
intervals = [[0,30],[5,10],[15,20]]
min_meeting_rooms -> 2
assign_rooms      -> [0, 1, 1]   # [5,10] 和 [15,20] 都可以用房间1（不冲突，复用）
```

**例 2**（LC 官方例 2：不重叠只需 1 间）
```
intervals = [[7,10],[2,4]]
min_meeting_rooms -> 1
assign_rooms      -> [0, 0]
```

**例 3**（半开区间：挨着的端点不冲突）
```
intervals = [[1,5],[5,10]]
min_meeting_rooms -> 1              # 5 点结束、5 点开始不冲突
assign_rooms      -> [0, 0]         # 同一间房复用
```

**例 4**（"最小空闲房间号优先"生效）
```
intervals = [[0,5],[0,5],[1,2],[6,7]]
# 前两个会议同时开始，各占一间（房间0、房间1）；第三个会议 [1,2] 与前两个都冲突，只能开新房间2
# 第四个会议 [6,7] 此时房间0、1、2 都已经空出来了，选编号最小的房间0
assign_rooms -> [0, 1, 2, 0]
```

**例 5**（容量匹配：小会议不能用小房间时才占用大房间）
```
meetings = [(0,10,3), (1,2,1), (2,3,1)]
capacities = [1, 3]     # 房间0容量1，房间1容量3
# 第一个会议要容量>=3，只有房间1能用；第二、三个会议只需要容量>=1，房间0全程可用
assign_rooms_with_capacity -> [1, 0, 0]
```

**例 6**（房间数不够，贪心也无力回天：3 个同时段的大会议只有 2 间够格的房间）
```
meetings = [(0,5,3), (0,5,3), (0,5,3)]
capacities = [3, 3]
assign_rooms_with_capacity -> [0, 1, None]
```

## `main()` 命令流

```
PART 1              PART 2              PART 3
N 3                 N 3                 N 3
0 30                0 30                0 10 3
5 10                5 10                1 2 1
15 20               15 20               2 3 1
→ 2                 → 0                 C 2
                       1                 1
                       1                 3
                                         → 1
                                           0
                                           0
```

## 边界清单

- 空区间列表 → `min_meeting_rooms` 是 0，`assign_rooms` 是 `[]`
- `start >= end`（含 `start == end` 的零长会议）→ `ValueError`：本题要求正时长，避免"零长会议算不算占用房间"这种没有统一约定的灰色地带
- 半开区间边界：结束时间等于下一个开始时间不算冲突（例 3，容易和 pc05 的闭区间约定搞混）
- 同一开始时间的多个会议：Part 2 按原始下标 tie-break，保证同样输入总是同样输出
- "最小空闲房间号优先"：不是"最近释放的房间优先"，也不是"轮转分配"（例 4）
- Part 3：`capacity < 0`、`size <= 0`、`start >= end` → `ValueError`
- Part 3：容量相同时选房间号最小的（例 6 两个 cap=3 的房间，先给房间0）
- Part 3：房间数量/容量不够时该会议是 `None`，不影响后续会议的处理
- 大规模：20 万条区间要在 2 秒内跑完（双指针/堆实现，不能是 O(n²)）

## 追问

1. **为什么 pc05 是闭区间、这题是半开区间？** 两种约定在业界题库里都存在，面试时第一件事应该是明确问清楚"挨着的端点算不算冲突"；本题按 LC 253 的标准约定（半开）来实现，并在题面显式对比，避免混用。
2. **"最小空闲房间号"这个规则有什么实际意义？** 对应真实场景里"房间号越小通常越靠近入口/越常用"，把利用率集中到编号靠前的房间，方便清洁/维护调度只需要盯着少数几个高频房间。
3. **Part 3 的贪心具体在什么场景下会不是最优？** 典型反例是"按开始时间在线处理"这个框架本身的局限——一旦某个会议被处理并分配了房间，就不能因为后面出现更紧迫的会议而重新调整；只要允许"先看到的会议不一定先分房间"（离线全局匹配），有时能避免在线贪心里出现的 `None`。这是一个二分图匹配加时间窗约束的问题，精确求解是 NP-hard。
4. **能不能把 Part 2 的"新增房间"上限设死（比如最多 N 间）？** 那就变成了 Part 3 的固定房间数版本，只是没有容量区分（所有房间容量相同、所有会议规模相同）。
5. **会议可以取消/重新安排吗？** 本题的两个 part 都是"一次性给定全部会议，离线处理"；如果要支持动态插入/取消，Part 2 的两个堆结构可以直接扩展支持"提前结束"事件，但要额外处理"取消一个尚未处理的会议"这种情况。

## 来源与置信度

- **LOW（页面登录墙，仅一句话摘要）**：https://www.1point3acres.com/interview/post/7546739，"Snowflake 2026 Software Engineer Intern VO Interview Experience"，WebFetch 摘要："a meeting room scheduling problem to find the minimum rooms required for overlapping requests"，标注为该 2026 届实习技术面的原题。正文在登录墙后未能核实具体例子/数据规模。见 `../../../../catalog/raw/coding_phone_onsite.md` #27。对应 LC 253 Meeting Rooms II 题族。
- Part 2（分配具体房间号）、Part 3（房间容量匹配）未见一手报道，按会议室调度类题目最常见的追问方向重建，已在题面标注 **(reconstructed)**。
- LC 253 官方题面（订阅题，无公开链接）：题号 253 "Meeting Rooms II"。

## 考什么

S03（区间调度，与 pc05 对照：半开 vs 闭区间的边界严谨性）· 双堆模拟资源分配的确定性 tie-break 设计 · 诚实标注贪心算法的局限性，而不是假装它是最优解。
