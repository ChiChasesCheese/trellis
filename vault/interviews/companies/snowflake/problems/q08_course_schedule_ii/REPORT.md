# q08 Course Schedule II — report

## 摘要

Part1 是 LC 210「Course Schedule II」的逐字原题复用（Snowflake OA 题库 2023 Canada index item
#14），标准拓扑排序，唯一的"坑"是它要求 **确定性输出**，所以额外加了一条题库没有强制但为了可测试性
必须有的规则：可选课程集合用最小堆维护，永远先修编号最小的课。Part2 是根据题库引用的 LC1136
"Parallel Courses" 形状原创的 follow-up ——"最少并行学期数"，本质是同一个 Kahn 拓扑排序算法，只是
按层（BFS layer）计数而不是逐个出队。两部分共享"拓扑排序 + 环检测"的核心技能，但故意用了两套不同
的下标习惯（Part1 0-indexed，Part2 1-indexed）来强迫候选人读清楚每个函数自己的输入约定，而不是想
当然地套用同一套代码。

## 来源与置信度

- Part1：https://leetcode.com/problems/course-schedule-ii/ （LC 210，MED，OA 题库原题，2023 Canada
  index item #14）—— 高置信度，逐字复用，题面英文引用见 problem.md。
- Part2：题库仅给出"引用 LC1136/LC2050，无逐字题面"的说明。本报告的 Part2 是我按 LC1136 题意精确
  形式化的产物，**非逐字复原**，但直接扎根于题库的具名引用，不算凭空编造。三个 worked example
  （diamond=3学期、环=-1、无依赖=1学期）都是我手算并用独立脚本验证过再写进测试的。置信度：中。

## 逐 part 思路

- **Part1**：建邻接表 `adj[b] -> a`（`prerequisites[i]=[a,b]` 表示 a 需要 b），统计入度；把所有
  入度为 0 的课程放进一个 min-heap；每次弹出堆顶（最小编号）加入结果，并把它解锁的后继课程的入度
  减一，一旦降到 0 就压入堆。最后如果结果长度等于 `num_courses` 就返回，否则说明有环，返回 `[]`。
- **Part2**：同样的 Kahn 算法，但改用 BFS 分层：每一轮把当前队列里的所有课程（同一层，可并行修）
  全部处理完，学期数 +1；处理时把它们的后继入度减一，归零的加入下一轮队列。处理的课程总数等于
  `num_courses` 才是有效解，否则是环，返回 `-1`。`num_courses=0` 时队列一开始就是空的，`semesters`
  保持 0，`taken==num_courses(=0)` 成立，正确返回 `0`（不是 `-1`）。

## 隐藏测试针对的坑

- **tie-break 必须是最小堆而不是任意拓扑序**：`test_min_heap_tiebreak_smallest_id_first` 专门构造
  两条独立链，验证多门课同时入度归零时输出严格按最小编号出堆，而不是依赖遍历顺序或插入顺序的偶然
  一致。
- Part1 和 Part2 的下标习惯不同（0-indexed vs 1-indexed）：直接把 Part1 的代码复制到 Part2 而不
  调整下标范围会导致 `IndexError` 或漏掉编号为 `num_courses` 的课程（起草时用脚本先验证了这一点，
  才把 Part2 的邻接表/入度数组大小定为 `num_courses+1`）。
- Part2 `num_courses=0` 容易被误判为 `-1`（"没有课程所以无法完成"），实际应为 `0`（0 个学期，因为
  没有课程要修）。
- Part1/Part2 都要能识别自环 `[[0,0]]` / `[[1,1]]` —— 自环让对应课程入度恒为 1，永远进不了 ready
  集合，触发环检测路径。
- 长链（每门课依赖上一门）在 Part1 下会强制唯一顺序（tie-break 规则实际上不影响结果），在 Part2 下
  产生 n 个学期 —— 用来验证两个 part 在退化到"没有并行空间"时依然正确。

## 复杂度与实测

两个 part 都是标准 Kahn 算法：O(V+E) 时间、O(V+E) 空间；Part1 额外有堆操作，是
O((V+E) log V)。perf 测试把图规模定在 **2 万节点**（而不是题面通用的 1e5-1e6），因为这是图/树类
问题（拓扑排序、BFS）而非"扁平记录流"类问题 —— 2 万节点 × 每节点 1-3 条边（约 4-5 万条边）已经能
在 Python 里充分体现 O(E log V) vs O(E) 的差距，同时把总测试时间控制住；本地实测 2 万节点随机 DAG
的 Part1 拓扑排序 + stdin/stdout 往返约 0.1-0.2s，远低于 2s 预算。Part2 用了 200 层的分层随机图
（同样 2 万节点规模）验证纯 BFS 分层同样在预算内。

## 测试清单

22 个测试 —— part1: 12 个（含 2 个 io、1 个 perf、1 个 fmt）；part2: 10 个（含 1 个 io、1 个
perf）；edge 10 个（覆盖 0 门课、单门课、自环、长链、不连通分量）。全部针对 `solution.py` 通过；
针对 `starter.py`（`IMPL=starter`）确认产生 17 个真实断言失败（并非 collection error），其余 5
个恰好因为 stub 的 `[]`/`0` 返回值巧合命中了对应边界期望而"意外通过"，这是边界值本身的巧合，不
影响 suite 整体能否区分正确/错误实现的能力。

## 技能 ids

S05（图：拓扑排序、BFS 分层、valid tree / 环检测、确定性 tie-break）
