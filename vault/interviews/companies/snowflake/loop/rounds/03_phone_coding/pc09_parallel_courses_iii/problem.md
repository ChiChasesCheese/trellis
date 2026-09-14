# pc09 · Parallel Courses III（LC 2050）— 带权 DAG 上的关键路径

> Onsite 题。Part 1 是一手报道的原题，题号和例子逐字匹配；Part 2 是给出一条具体关键路径的常见追问，**(reconstructed)**。

## 背景

一份 onsite 面经明确标出 **LC 2050 Parallel Courses III，未改动**：`n` 门课、先修关系对、每门课耗时，任意多门无冲突依赖的课可以同时上，求修完全部课程的最短时间。原帖给出的例子（`n=5, relations=[[1,5],[2,5],[3,5],[3,4],[4,5]], time=[1,2,3,4,5] → 12`）与 LC 官方例 1 完全一致。

这类题真正的坑不是"要不要用拓扑排序"，而是：**编号是 1-based（`relations`）还是 0-based（`time`）容易搞反**、**5×10^4 长的依赖链下递归会爆栈**、**"关键路径"不是随便一条最长依赖链，而是与总耗时严格挂钩、可能有平手需要判定字典序**。

## 输入

- `n ≥ 1`：课程数，编号 `1..n`。
- `relations`：`[prevCourse, nextCourse]` 列表（**1-based**），`prevCourse` 必须先于 `nextCourse` 完成才能开始。
- `time`：长度为 `n` 的列表（**0-based**，`time[i]` 对应课程 `i+1`），每门课耗时 `≥ 1`。
- `relations` 必须构成 DAG；含环、自环、编号越界、`time` 长度不对、耗时非正 → 抛 `ValueError`。

## API 契约（英文签名）

```python
def minimum_time(n: int, relations: list[list[int]], time: list[int]) -> int
def critical_path(n: int, relations: list[list[int]], time: list[int]) -> tuple[int, list[int]]
```

## 规则

### Part 1 — 最短完成时间（LC 2050 原题）

用 Kahn 拓扑扫描算 `finish[v] = time[v] + max(finish[u] for u in v 的先修课程)`（没有先修课程时是 `0`），答案是 `max(finish)`。**必须写成迭代版**：LC 官方压力测试里有长度 5×10^4 的依赖链，递归 DFS 会栈溢出。

### Part 2 — 给出一条关键路径 **(reconstructed)**

返回 `(最短完成时间, 一条关键路径的课程编号列表)`。"关键路径"是一条先修链 `c1 → c2 → ... → ck`（每一步都是直接先修关系），满足 `sum(time[cj-1] for cj in path) == minimum_time(...)`。可能有多条并列的关键路径，**取字典序最小的那一条课程编号序列**（逐位比较；若一条是另一条的前缀，更短的那条更小——不过由于每个节点的最优后缀在算法里是唯一确定的，这种前缀关系在本题结构下不会真的出现）。

**复杂度/规模提示**：字典序最小路径的重建需要在有并列关键路径时逐位比较候选序列，最坏情况下开销与"节点数 × 平均候选序列长度"相关。Part 2 的测试规模控制在 `n ≤ 3000` 左右，足以覆盖平手判定，但不重复 Part 1 的 5×10^4 规模压测。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1**（onsite 面经原例 = LC 2050 官方例 1）
```
n = 5, relations = [[1,5],[2,5],[3,5],[3,4],[4,5]], time = [1,2,3,4,5]
minimum_time  -> 12
critical_path -> (12, [3, 4, 5])   # 课 3 (耗时3) -> 课 4 (耗时4) -> 课 5 (耗时5)，3+4+5=12
```

**例 2**（没有任何先修关系，各课独立）
```
n = 3, relations = [], time = [5, 3, 8]
minimum_time  -> 8                  # 最长的一门课决定总时间
critical_path -> (8, [3])
```

**例 3**（两条互不相干的链打平手，取字典序小的）
```
n = 4, relations = [[1,2],[3,4]], time = [1,5,2,4]
# 链 1->2：1+5=6；链 3->4：2+4=6，打平
minimum_time  -> 6
critical_path -> (6, [1, 2])        # [1,2] 字典序小于 [3,4]
```

**例 4**（菱形 DAG，两条路径到达同一节点耗时相同）
```
n = 4, relations = [[1,2],[1,3],[2,4],[3,4]], time = [1,2,2,3]
# 1->2->4 = 1+2+3=6；1->3->4 = 1+2+3=6，打平，第二步 2 < 3
minimum_time  -> 6
critical_path -> (6, [1, 2, 4])
```

## `main()` 命令流

```
PART 1                      PART 2
5 5                         4 2
1 5                         1 2
2 5                         3 4
3 5                         1 5 2 4
3 4
4 5
1 2 3 4 5
→ 12                        → 6
                              1 2
```

## 边界清单

- `relations` 的编号是 1-based，`time` 是 0-based —— 两个方向都要测到
- 无任何 `relations`（每门课独立）→ 答案是 `max(time)`
- 单门课 `n = 1`
- 含环 → `ValueError`，报错信息要说明是环而不是别的输入错误
- 自环 `[u, u]` → `ValueError`
- 课程编号越界（`0` 或 `> n`）→ `ValueError`
- `time` 长度与 `n` 不符 / 含非正数 → `ValueError`
- 多条并列关键路径：不同起点打平手（例 3）、同一起点不同延伸打平手（例 4）
- Part 1 在 5×10^4 长依赖链下不爆栈、2 秒内跑完
- Part 2 在 `n ≈ 3000`、平手较多的稠密 DAG 下 2 秒内跑完

## 追问

1. **为什么按 `finish` 值降序处理节点就能保证子问题已经算好？** 一条"紧邻边" `(u, v)`（`finish[v] == finish[u] + time[v]`）必然满足 `finish[v] > finish[u]`（因为 `time[v] ≥ 1`），所以按 `finish` 降序处理时，任何节点的后继都已经处理完毕。
2. **关键路径一定经过耗时最长的单门课吗？** 不一定，例 4 里耗时最长的是课 4（3），但真正的关键路径还包括耗时短的课 1、2；决定总时长的是链的和，不是链上某一门课。
3. **k 个工位、最多同时上 k 门课，怎么排？** 经典 list scheduling：按"到终点最长剩余链"（在反图上再跑一次本题的 DP）排优先级，事件驱动模拟空位释放；这是 NP-hard 问题的启发式近似，不保证最优（Stripe 同族题 `qA09` 的 Part 3 就是这个套路，本题不展开）。
4. **如果 `time[i]` 可以是 0？** 允许的话 `finish` 不再严格递增，关键路径重建那一步的降序处理顺序就要改成"先按 finish 降序、finish 相同时随意但要保证同一层内没有相互依赖"；本题按 LC 约束 `time[i] ≥ 1` 排除了这个复杂度。
5. **能不能边读边算（流式先修关系）？** 一般不行——`finish[v]` 依赖所有先修课程都已知，必须等图完整后再跑一次全局拓扑排序；除非保证先修关系按拓扑序到达。

## 来源与置信度

- **MED-HIGH（题号 + 例子逐字匹配 + 明确 onsite 标签）**：https://www.fastprep.io/problems/snowflake-parallel-courses-iii（Hard，Snowflake Fulltime Onsite Interview，Graph）。题面与例子（`n=5, relations=[[1,5],[2,5],[3,5],[3,4],[4,5]], time=[1,2,3,4,5] → 12`）与 LC 2050 完全一致。见 `../../../../catalog/raw/coding_phone_onsite.md` #25。
- Part 2（给出关键路径）未见一手报道，按最长路 DP 类题目最常见的追问方向重建，已在题面标注 **(reconstructed)**；写法参考了 Stripe kit 同源题 `qA09_lc2050_parallel_courses_iii` 的思路（Kahn + 关键路径回溯），但题面、字典序最小规则与测试均为本题独立编写。
- LC 2050 官方题面：https://leetcode.com/problems/parallel-courses-iii/

## 考什么

S05 图：拓扑排序 / DAG 上的最长路 DP · 迭代改写避免递归栈溢出（5×10^4 长链）· 平手判定的确定性字典序规则设计。
