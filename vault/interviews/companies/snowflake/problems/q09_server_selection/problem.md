# q09 · Server Selection with switching cost — **(reconstructed)**

**Type:** OA · **Stage:** OA · **Last asked:** 2022-09-08 / 2022-11-08 posts, indexed as 2023
Canada list item #2 · **Confidence:** MED (image-only source, complexity constraint is the only
hard detail recovered)

> ⚠️ **本题整体标记为 (reconstructed)**：两个已知来源帖子都只有截图、没有文字题面，其中一条评论
> 恢复出了唯一的文字线索——一个复杂度约束。下面 Part1 / Part2 的每一条规则标题都会再次标注
> **(reconstructed)**，因为整道题的具体设定（cost 结构、switch_cost 语义、tie-break 规则）都是
> 我根据这条复杂度线索**设计**出来的一个自洽、可测试的问题，不是逐字复原。

## 背景

来源只确认了："m 个 server，n 个 item，2D DP，目标复杂度 O(m·n)，对比一个更慢的 O(N^2) 量级解法"。
本题把这个线索具体化为一个"server 切换有代价"的经典 DP 问题：这类问题天然存在一个"朴素解 O(m²n)"
和一个"优化解 O(mn)"的复杂度落差（用 best/second-best 技巧把每格的转移从 O(m) 降到 O(1)），跟来源
帖子里评论提到的复杂度落差完全吻合。

## 输入格式（stdin，`main()`）

```
PART 1|2
m n switch_cost
cost[0][0] cost[0][1] ... cost[0][n-1]
cost[1][0] ... cost[1][n-1]
...
cost[m-1][0] ... cost[m-1][n-1]
```
（`n=0` 时没有任何 cost 行。）

## 规则

### Part 1 — 朴素 O(m²n) 解 **(reconstructed)**

`part1(m: int, n: int, cost: list[list[int]], switch_cost: int) -> int`

有 `m` 个 server 和 `n` 个按顺序 `0..n-1` 处理的时间槽。`cost[j][i]` 是"第 `i` 个时间槽让 server `j`
处于激活状态"的代价（一个 `m x n` 的二维数组）。`switch_cost` 是一个固定的额外代价，只要**相邻两个
时间槽之间激活的 server 发生变化**就要付一次（槽 0 没有"上一个状态"，所以槽 0 选任何 server 都不
付切换代价）。每个时间槽恰好激活一个 server。求 `n` 个时间槽的总代价最小值。

"朴素但慢"的做法：对每个时间槽、每个 server，扫描**所有**其他 server 在上一个时间槽的最小总代价
（每格 O(m)）——总复杂度 O(m²n)，当 `m` 接近 `n`（来源约束 `m<=n<=1000` 暗示的场景）时，这就是来源
里提到的"O(N²)"量级基线。

### Part 2 — 优化 O(mn) 解 + 路径重建 **(reconstructed)**

`part2(m: int, n: int, cost: list[list[int]], switch_cost: int) -> tuple[int, list[int]]`

签名和语义与 Part1 相同，但**必须**做到真正的 O(m·n)：对每个时间槽，只需要追踪上一个时间槽所有
server 里的**最优**和**次优**总代价（以及最优是哪个 server 达成的）——这样 server `j` 在当前槽的
最佳"切入"前驱代价就是：

- 如果上一槽的最优 server **不是** `j`：`前一槽最优代价 + switch_cost`
- 如果上一槽的最优 server **正是** `j`（不能"切换到自己"）：`前一槽次优代价 + switch_cost`

再跟"不切换"选项（`上一槽 server j 自己的代价`，无 switch_cost）比较取更小者。这把每格的转移代价
从 O(m) 降到 O(1)，总复杂度 O(m·n)。

Part2 **还必须**能返回选择的 server 序列：返回 `(min_total_cost, assignment)`，其中
`assignment[i]` = 达成最小总代价所选择的、第 `i` 个时间槽激活的 server 下标。

**Tie-break 规则（必须严格遵守，否则 assignment 对不上样例）**：

1. 当"不切换"（停留在上一槽同一个 server）的代价，和"切换"的最佳代价打平时，**优先选择不切换**。
2. 如果还是打平（比如槽 0 没有"上一槽"概念可比较，或者多个 server 打平且没有明确的"前驱"可偏好），
   优先选择**编号最小**的 server。

## 样例（已用代码逐一验证，cost 和 assignment 都必须精确匹配）

```
m=2, n=3, cost=[[1,5,1],[4,1,1]], switch_cost=3
-> total=6, assignment=[1,1,1]
   (追踪：槽0 server0代价1/server1代价4，作为两条独立的起始状态。
   槽1: server0 = 5 + min(1[留在0], 4+3=7[从1切换]) = 5+1 = 6；
        server1 = 1 + min(4[留在1], 1+3=4[从0切换]) = 1+4 = 5 —— "留在1"(4) 和 "从0切换"(4) 打平，
        tie-break 选"不切换" -> 前驱是 server1@槽0。
   槽2: server0 = 1 + min(6, 5+3=8) = 7；
        server1 = 1 + min(5[留], 6+3=9[切]) = 1+5 = 6。
   最终 min(7,6)=6，来自 server1@槽2；回溯：server1@槽1（不切换，tie-break选择留下），
   server1@槽0。assignment=[1,1,1]，
   原始代价核对：cost[1][0]+cost[1][1]+cost[1][2] + 0次切换 = 4+1+1 = 6，与上面一致。)

m=2, n=1, cost=[[5],[2]], switch_cost=100
-> total=2, assignment=[1]
   (只有一个时间槽，不可能切换，直接选代价更低的 server。)

m=2, n=2, cost=[[1,100],[100,1]], switch_cost=1
-> total=3, assignment=[0,1]
   (全程留在同一个 server 代价是 1+100=101；切换一次代价是
   cost[0][0]=1 + switch_cost=1 + cost[1][1]=1 = 3，远优于不切换 —— 说明即使有切换代价，
   有时候切换仍然是最优的。)
```

## 隐藏测试边界清单

- `n=0`：总代价为 `0`，`assignment=[]`
- `m=1`：永远不可能切换，总代价 = 唯一那个 server 那一行的和
- `switch_cost=0`：切换永远免费，退化为每个时间槽独立选最小代价的 server
- `switch_cost` 很大（永远不值得切换）：退化为整段时间都停留在"整行总和最小"的那个单一 server（
  构造并验证过）
- Part1/Part2 在小规模（`m,n<=15`）下用随机数据交叉验证 `part1(...) == part2(...)[0]`
- perf：`m` 和 `n` 都约 1000（匹配来源约束 `m<=n<=1000`，共约 1e6 格），`part2`（O(mn)）要在 2 秒
  预算内轻松跑完；`part1`（记录为更慢的 O(m²n)）只在小规模的正确性测试里跑，**不**在满 1000x1000
  规模上做 perf 测试（见 REPORT.md 复杂度部分的诚实说明）

## 变体

- `switch_cost` 因 server 对而异（`switch_cost[j][k]` 矩阵而非单一常数）——会破坏 best/second-best
  的 O(1) 转移技巧，需要换成别的优化方向。
- 允许"停机"（不激活任何 server，付固定 idle 代价）——多加一个虚拟 server 即可复用同一套 DP。
- 只要求 Part1 的朴素解（有些帖子的评论暗示面试官只考到"能写出 O(N²)"就够，O(m·n) 是加分追问）。

## 来源与置信度

- https://leetcode.com/discuss/interview-question/2594968/Snowflake-or-OA-or-Server-Selection
  （2022-09-08，纯截图，评论者报告"没能解出来"）
- https://leetcode.com/discuss/interview-question/2794537 （2022-11-08，"Server Selection"，同样
  纯截图，但有一条文字评论给出："2 <= m <= n <= 1000... there is an O(N^2) solution, but [asking]
  how to solve in O(m*n)"）
- 索引为 2023 Canada list item #2
- 置信度：中（纯截图来源，唯一能恢复的硬信息是这条复杂度约束；具体的 cost/switch_cost 设定和三个
  worked example 都是我设计并用代码验证过的，不是逐字复原）

## 考什么

skills: S08（LC 原题变体 + 复杂度再压一档：这里是 O(m²n) → O(m·n) 的 best/second-best DP 优化）·
路径重建 + 确定性 tie-break · 小规模暴力交叉验证优化解的正确性
