# 任务调度器 II（Task Scheduler II, LC 2365）

有一串任务，每个任务有一个类型，必须**按给定顺序**一个接一个完成。每天只能做一个任务，或者休息。同一类型的两个任务之间必须至少隔 `space` 天。问做完所有任务最少需要多少天。它和 LC 621 的差别在于：621 允许重排任务，这里顺序固定，所以不需要任何贪心排序，只要知道每种类型上次是哪一天做的。

## 题面与约束
`tasks[i]` 是第 i 个任务的类型，必须按顺序完成；每天做一个任务或休息；同一类型的两个任务之间至少间隔 `space` 天。求完成所有任务的最少天数。
约束：`1 <= tasks.length <= 10^5`，`1 <= tasks[i] <= 10^9`，`1 <= space <= tasks.length`。

## 开场先问的澄清问题
1. 「间隔 space 天」是中间隔 space 天，还是两次相差 space 天？（题意是中间隔 space 天，即相差 space + 1。）
2. 任务必须按顺序吗？（是，这是与 621 的根本区别。）
3. 类型取值很大（到 1e9），是不是只能用哈希表？

## 先补一点基础：哈希表记「最后一次时间」
哈希表（hash map）把键映射到值，平均 O(1) 读写。这里键是任务类型，值是它上次执行的那一天。类型值到 1e9，数组放不下，哈希表只存出现过的类型。

## 最笨解
一天一天模拟：每天看当前任务的类型在最近 `space` 天里是不是出现过，出现过就休息，否则执行。正确，但如果 `space` 很大、任务很少，每天都要回看 `space` 天，是 O(天数 × space)；天数可达 n·space 量级，约 1e10，超时。（见代码里的 `_brute`。）

## 逐步改进
1. **问题**：回看窗口太贵、天数本身也可能很大（休息天是一天天累加的）。
2. **想法**：不模拟每一天，只记录「每种类型上次执行的天」。执行任务 t 时，最早能做的一天是 `last[t] + space + 1`；同时至少比上一个任务晚一天（`day + 1`）。
3. **为什么有效**：任务顺序固定，所以「当前天数」只由前一个任务和同类型的上一次决定，不需要关心中间发生了什么。取两者的最大值，休息的天数直接「跳过」，不逐天循环。

```python
def task_scheduler_ii(tasks, space):
    last = {}                                             # task type -> day it last ran
    day = 0
    for t in tasks:
        day += 1                                          # at least one day passes per task
        if t in last:
            day = max(day, last[t] + space + 1)           # need a gap of `space` days between equal types
        last[t] = day
    return day
```

示例：`tasks=[1,2,1,2,3,1], space=3`：第 1、2 天做 1、2；第二个 1 要等到第 1+3+1 = 5 天；第二个 2 要等到 2+4 = 6 天；3 在第 7 天；最后的 1 要等到 5+4 = 9 天，答案 9。`[5,8,8,5], space=2`：5(1) 8(2) 8 需要 2+3 = 5 天，5 需要 1+3 = 4，但已排到第 6 天，答案 6。

## 复杂度
时间 O(n)，空间 O(k)，k 是不同类型数。

## senior 追问
1. **任务可以重排（回到 621）**：贪心 + 最大频次，公式 `(maxFreq-1)*(space+1)+countMax`；这是「顺序固定」与「顺序自由」的本质区别。
2. **返回具体的每天安排**：保留每个任务实际执行的天，和休息的天。
3. **流式任务（不知道总长）**：同一个算法，在线一个一个喂，状态只有 `last` 与 `day`。
4. **类型很多、内存吃紧**：`last` 可以只保留「还没过冷却」的类型（用队列按到期时间清理），内存 O(space)。
5. **不同类型有不同冷却时间**：`space` 变成 `space[type]`，同一个公式。
6. **多机器并行**：每台机器一个独立的 `day`；任务分配变成调度问题，通常用最小堆维护各机器空闲时间。

## 自测题
1. 为什么 `day += 1` 在 `max` 之前？
<details><summary>答案</summary>每个任务至少占一天，即使没有冷却限制，也要比上一个任务晚一天。</details>
2. `last[t] + space + 1` 里为什么要 +1？
<details><summary>答案</summary>要求中间隔 `space` 天，所以两次相差 `space + 1`。</details>
3. 最后一次任务完成日就是答案吗？
<details><summary>答案</summary>是，最后一天做完最后一个任务，之后不再需要休息。</details>

## 来源
- Hello Interview 社区题目 `task-scheduler-ii`，约 2026-09-10，Staff：https://www.hellointerview.com/community/questions/task-scheduler-ii ；公司页 https://www.hellointerview.com/community/questions?company=Amazon 。
- 摘要：「find the minimum total days (including required breaks) to finish all tasks while ensuring any two tasks of the same type are separated by at least space days」。报告只有题目名和级别，没有追问。
- LC 官方 https://leetcode.com/problems/task-scheduler-ii/ （约束取自该页）。
- 代码：`../../coding/solutions/2365_task_scheduler_ii.py`。与已有的 LC 621 Task Scheduler 不同：这里任务必须按给定顺序执行。
