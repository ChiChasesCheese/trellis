# q01 · Task Scheduling — paid server vs free server

**Type:** bespoke OA · **Stage:** Online Assessment · **Last asked:** 2026-03 (Snowflake OA, per
LeetCode Discuss) · **Frequency:** 3 independent mentions · **Confidence:** high

## 背景

Snowflake 的 OA 里反复出现一道"两台机器抢任务"的题：一台**付费机**(paid server)，一台**免费机**
(free server)。任务按数组下标顺序、逐个到达（第 i 个任务在"时间 i"到达，这一点是让免费机固定
"1 单位时间"这句话有意义的关键——它把任务顺序和时间轴绑在一起）。付费机同一时刻只能处理一个任务；
免费机不管任务本身多"重"，处理一个任务永远只花 1 单位时间、不要钱。

## 原题引用（verbatim）

> You are given two arrays, cost and time. You have a paid server, and a free server. You
> receive the tasks in order from left to right. For the ith task, if there is no task already
> running on the paid server, you must schedule the new task on the paid server. Otherwise, you
> can choose to schedule the task on the paid server or the free server. cost[i] represents the
> cost of performing the ith task on the paid server, and time[i] represents the time it takes
> to perform the ith task on the paid server. It costs nothing to schedule a task on the free
> server, and the free server processes the ith task in 1 unit of time, regardless of time[i].
> Return the minimum cost to schedule all tasks.

## 必须采用的精确模型（原题对"排队"语义含糊，下面是本题唯一自洽的读法，也是隐藏测试遵循的读法）

- 任务下标 `0..n-1`；任务 `i` 在时间 `i` "到达"（每个时间单位到达恰好一个任务）。
- 付费机维护一个计数器 `free_at`，初始为 `0`（时间 0 时付费机空闲）。
- 处理任务 `i` 时：
  - 若 `free_at <= i`（任务 i 到达时付费机空闲）：**必须**上付费机。`cost += cost[i]`；
    `free_at` 变为 `i + time[i]`（从"现在"算起跑 `time[i]`）。
  - 若 `free_at > i`（付费机还在忙，有积压）：**可以选**：
    - (a) 上免费机：`cost += 0`，`free_at` 不变；或
    - (b) 排队上付费机：`cost += cost[i]`；`free_at += time[i]`（在原本排队到的时间点之后，再接
      着跑 `time[i]`）。
- 目标：让全部 n 个任务都被处理完的**最小总成本**。`n` 最多 `1e5`；`cost[i]`、`time[i]` 均为
  `0..1e9` 的非负整数。

## 输入格式（stdin）

```
PART <1|2>
n
cost[0] cost[1] ... cost[n-1]
time[0] time[1] ... time[n-1]
```
第一行 `PART 1` 走 `part1`，`PART 2` 走 `part2`（两者对同一输入必须返回同一个数——这本身就是一类
隐藏测试）。`n = 0` 时，后两行可以是空行或直接省略。数组用空格分隔的整数。

## 输出（stdout）

一行：最小总成本（一个整数），末尾换行。

## 规则

### Part 1 — 直接/清晰解（不要求 n=1e5 性能）
用最直白的方式实现上面的模型：对每个"忙碌"状态做二选一的递归/DP，`n` 较小（题目里给的例子都
`<=3`）时保证正确即可。可以是未剪枝的记忆化搜索。

### Part 2 — 满足 n 达到 1e5 的性能预算
`part2` 对同一输入必须和 `part1` 返回完全相同的数字，但要能在性能预算内跑完 `n` 达到题目声称的
规模（见下方"复杂度与实测的偏差说明"——这题的精确解在最坏情况下没有已知的亚二次算法，实测中
even 均匀随机数据也会让状态数随 n 线性增长，使得下面这个"剪枝 frontier"整体是 O(n·状态数)，
详见 REPORT.md）。

思路：对"付费机何时空闲"（`free_at`）维护一个**前沿（frontier）**：`{free_at: 到达这个状态的最小
成本}`。每一步：
- 把 frontier 按 `free_at <= i`（会被强制上付费机）与 `free_at > i`（忙碌，可选）分成两组。
- 强制组：无论各自原来的 `free_at` 是多少，这一步的转移完全一样，所以**先取强制组里的最小成本**
  一次性算出唯一的新状态 `(i + time[i], min_cost + cost[i])`。
- 忙碌组：每个状态 `(free_at, c)` 分裂出两个候选后继：`(free_at, c)`（选免费机）和
  `(free_at + time[i], c + cost[i])`（排队付费机）。
- 剪枝：合并所有候选后继后，**按 `free_at` 从大到小排序，只保留成本严格小于「目前为止（更大或相等
  free_at 里）见过的最小成本」的状态**——也就是说 `free_at` 更大、成本更低或相等的状态，支配
  `free_at` 更小、成本更高或相等的状态。

  ⚠️ **注意剪枝方向**：直觉上容易想反成"`free_at` 更小更好"（毕竟"早点忙完"听起来是好事），但
  实际推导（也用暴力交叉验证过，见 `test_q01.py::test_part1_part2_agree_random`）说明**方向是反的**：
  `free_at` 更大（更忙）在未来永远只会给你更多选择——它能通过"也选择付费"来至少模拟一个更小
  `free_at` 状态接下来的强制转移；反过来，`free_at` 更小、更早空闲的状态，可能会在未来某个时刻被
  强制上付费机而无法选择免费机，从而付出一笔本可避免的成本。所以是"**更大的 `free_at` + 更低或相等
  的成本**"支配"更小的 `free_at` + 更高或相等的成本"，不是反过来。
- 最终答案 = 剪枝后 frontier 里成本的最小值。

## Worked Examples（手算验证）

1. `cost=[1,2], time=[1,2]` → **3**
   任务0：`free_at(0)<=0` 强制付费：`cost=1`，`free_at=1`。
   任务1：`free_at(1)<=1` 依然强制付费：`cost=1+2=3`，`free_at=1+2=3`。全程没有选择权。

2. `cost=[5,1], time=[3,1]` → **5**
   任务0：强制付费：`cost=5`，`free_at=3`。
   任务1：`free_at(3)>1`，忙碌，有选择：上免费机花 `0`（总 `5`）；排队付费机要花 `1`（总 `6`，更差）。
   选免费机，答案 `5`。

3. `cost=[5,100,1], time=[3,1,1]` → **5**
   任务0：强制付费：`cost=5`，`free_at=3`。
   任务1：`free_at(3)>1`，忙碌；任务2：`free_at(3)>2`，忙碌。两个都送免费机各花 `0`。任何其他组合
   都更贵（比如任务1排队要 `+100`）。答案 `5`。

4. **"排队反而更划算"的例子**（隐藏测试常考的坑）：`cost=[1,1,1000], time=[2,1,1]` → **2**
   任务0：强制付费：`cost=1`，`free_at=2`。
   任务1：`free_at(2)>1`，忙碌，有选择：
     - 选免费机：`cost=1`，`free_at` 仍是 `2` → 任务2到达时 `free_at(2)<=2`，**被迫**强制付费
       `+1000`，总成本 `1001`。
     - 排队付费：`cost=1+1=2`，`free_at=2+1=3` → 任务2到达时 `free_at(3)>2`，仍然忙碌、有选择，
       可以放心送免费机，总成本 `2`。
   **排队上付费机反而更便宜**（省了 `999`），因为它把付费机的空闲点推迟到了任务2之后，让任务2
   避免被强制收取天价 `cost[2]=1000`。

## 隐藏测试边界清单

- `n = 0`（空数组）→ 答案 `0`。
- `n = 1`（单任务）→ 永远强制付费 → 答案就是 `cost[0]`。
- `cost[i] = 0` 或 `time[i] = 0`：`time[i]=0` 意味着这个任务处理完付费机立刻又空闲（`free_at`
  不往前推进），可能导致下一个任务也被强制。
- `cost[i]`、`time[i]` 取到 `1e9` 级别的大数：必须用精确整数，不能有任何浮点参与。
- "排队反而更划算"的构造（见 worked example 4）——`part1`/`part2` 必须都算对，且两者结果一致。
- `part1` 与 `part2` 在随机小规模（`n<=12`）输入上必须给出完全相同的答案（交叉验证测试）。
- `PART` 行大小写、多余空格的容忍度；`n=0` 时数组行缺失或为空行都要能正确解析。

## 变体

- 部分版本里 free server 的"1 单位时间"会影响到*后续免费任务*的调度（即免费机也可能"忙"）——
  本题按原题字面意思，免费机永远瞬间可用，不建模免费机的忙闲。
- 有的转述版本让候选人只需要返回总成本（函数式），不需要写 stdin/stdout；这里通过 `PART` 行 +
  `main()` 同时覆盖两种形式。

## 来源与置信度

- https://leetcode.com/discuss/interview-question/2550834/Snowflake-OA-(CoreData-Engineering-Intern)
  — 2022-09-08，Core/Data Engineering Intern OA，题面逐字一致。**HIGH**。
- https://www.linkjob.ai/interview-questions/snowflake-software-engineer-interview/ — 2026-03-16，
  独立提到 "Task Scheduling – 0/1 knapsack variation optimizing costs across paid and free
  servers"。**MED**（佐证同一题族，非逐字）。
- https://leetcode.com/discuss/interview-question/2775415 — 2023 Canada intern 题目索引第1条
  （仅图片/链接佐证，未展开）。

## 考什么

skills: **S02** 计数/状态 DP（状态 = 位置 + 付费机剩余时间，取剪枝而非取模）· 精确整数计算
（禁止浮点）· 边界化简（forced vs choice 的转移合并）· 交叉验证测试思维（用一个简单解验证一个
复杂解）· 复杂度权衡的诚实表达（见 REPORT.md 的复杂度实测与偏差说明）。
