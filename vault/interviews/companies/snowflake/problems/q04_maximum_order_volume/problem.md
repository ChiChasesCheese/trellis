# q04 · Maximum Order Volume — weighted interval scheduling

**Type:** bespoke OA · **Stage:** OA · **Skill:** S03 (加权区间调度 / 排序 + 二分 + DP)

## 背景
一家超市接到很多通客户电话，每通电话有已知的开始时间、时长和这通电话对应的订单量
（order volume）。任意时刻超市只能处理一通电话（"only one call can be in progress at any
one time"）。目标是从所有来电中挑出一组互不重叠的电话，使被处理的订单量总和最大。

> "A supermarket receives customer calls with known start times, durations, and order
> volumes... only one call can be in progress at any one time... select non-overlapping
> calls to maximize total order volume."

题面给的函数签名是 `phoneCalls(start[], duration[], volume[]) -> int`；在本题里拆成
`part1`（正确但复杂度不作要求）和 `part2`（必须 O(n log n)）两版。

## 输入格式（stdin，用于 `main`）
```
PART <1|2>
n
start_1 duration_1 volume_1
start_2 duration_2 volume_2
...
start_n duration_n volume_n
```
`n` 可以是 0（此时没有后续数据行）。所有数值是非负整数；空行忽略。输出：单个整数
（末尾换行）。

## 规则
电话 `i` 占据半开区间 `[start[i], start[i]+duration[i])`。两通电话不重叠当且仅当其中一个
的结束时间 `<=` 另一个的开始时间（**端点相接算不重叠**，例如一通在 18 结束、下一通在 18
开始，这不算重叠）。从所有电话里选一个子集，使得互不重叠，且 `volume` 之和最大。

**`duration == 0` 的特殊情形**：这通电话占据的是空区间 `[start, start)`，里面不存在任何
点，所以无论它排在时间轴的什么位置，它都不会和任何别的电话冲突——即使它的时间点落在另一通
电话的区间内部。注意这**不是**用"结束 `<=` 开始"这条通用判定式就能自动得出的：比如一通
`duration=0` 的电话发生在 t=5，另一通电话是 `[0,10)`，两者既不满足 `10<=5` 也不满足
`5<=0`，如果直接套用两两判定式会误判为"重叠"。正确做法是把所有 `duration=0` 的电话的
`volume` **无条件**加总，再对其余（`duration>0`）的电话跑标准加权区间调度 DP，最终答案 =
无条件总和 + DP 结果。由于 `volume` 非负，这也保证了"最优解一定包含所有零时长电话"。

### Part 1 — 正确性优先
`part1(start: list[int], duration: list[int], volume: list[int]) -> int`：给出正确的 DP
解，不要求最优复杂度（例如按结束时间排序后，对每通电话线性或二分查找最近的不冲突前驱，
`dp[i] = max(dp[i-1], volume[i] + dp[pred[i]])`）。

### Part 2 — 大数据量
`part2(...)`：签名、语义与 `part1` 完全相同，但必须在 `n` 达到 `1e5` 时仍满足性能预算：
按结束时间排序 + 二分（`bisect`）查找前驱，总复杂度 `O(n log n)`。

## Worked Examples

**验证过的官方样例**（必须精确匹配）：
```
start    = [10, 5, 15, 18, 30]
duration = [30, 12, 20, 35, 35]
volume   = [50, 51, 20, 25, 10]
```
结束时间分别是 `40, 17, 35, 53, 65`。最优解是下标 1（`start=5, end=17, volume=51`）和下标
3（`start=18, end=53, volume=25`）：`end1=17 <= start3=18`，不重叠，总和 `51+25=76`。可以
逐一验证其他组合都不能超过 76。**答案：76**。

**样例 (a)：全部互相重叠** → 答案就是单个 volume 最大的电话：
```
start=[0,0,0,0], duration=[100,100,100,100], volume=[10,20,15,5] -> 20
```

**样例 (b)：全部互不重叠** → 答案是所有 volume 之和：
```
start=[0,10,20,30], duration=[5,5,5,5], volume=[1,2,3,4] -> 10
```

## 隐藏测试边界清单
- `n=0` → 返回 `0`；`n=1` → 返回 `volume[0]`
- 相同的 `start` 时间（并列开始，只能选一个）
- `duration=0` 的电话：必须被无条件计入总和，即使它的时间点落在另一通电话内部
- 多个 `duration=0` 电话同时存在，全部计入
- `start`/`duration`/`volume` 数值很大（用 Python int，绝不能引入 float 累加误差）
- 结束时间出现并列（排序需稳定，但由于二分查找的是"结束 `<=` 开始"，并列顺序不影响正确性）
- 端点相接（`end == start`）算不冲突

## 变体
- 有的题面把 `volume` 换成金额或优先级分数，逻辑不变。
- 有的变体要求同时返回被选中的电话下标列表，而不仅仅是总量（本题只要求总量）。

## 来源与置信度
- https://www.fastprep.io/problems/phone-calls （MED，题面与函数签名来源）
- https://leetcode.com/discuss/interview-question/1033329/snowflake-oa-intern/ （2021-01-25，仅标题佐证，原帖已 404）
- 2023 Canada OA 题库索引 #3（2023-02-10，同名题目再次出现）

**置信度：中** — 题面/样例来自 FastPrep 的公开描述，标题被两个独立来源交叉验证，但原始
LeetCode 讨论帖内容已失效，细节（如端点相接、zero-duration 的处理）是本题作者结合区间调度
的标准定义补全的，非题面逐字给出。

## 考什么
- S03：加权区间调度——排序 + 二分找前驱 + DP 转移
- 边界处理：半开区间、端点相接、零长度区间的"空集不相交"语义
- 整数运算：避免大数场景下的浮点误差
- 复杂度台阶：part1 正确优先，part2 卡 `O(n log n)` 的性能要求
