# q08 · Course Schedule II — topological order + minimum parallel semesters

**Type:** LC 210 exact reuse (Part 1) + original follow-up grounded in LC 1136 "Parallel Courses"
(Part 2) · **Stage:** OA · **Last asked:** 2023 Canada index item #14 · **Confidence:** high
(Part 1 verbatim LC reuse) / grounded-not-verbatim (Part 2, see 来源与置信度).

## 背景

Snowflake 的 OA 题库里直接搬运了 LeetCode 210「Course Schedule II」原题（拓扑排序求一个可行的选课顺
序）。题库的目录条目还标注了一道电面「prerequisite topological sort」的姊妹题，并引用了 LC 1136 /
LC 2050（"Parallel Courses" 系列）作为一个 follow-up 的方向说明 —— 没有找到这个 follow-up 的逐字题
面，但引用足够具体（就是"求最少并行学期数"这个形状），所以本题的 Part 2 是按 LC1136 的题意精确形式
化出来的（不是逐字复原，因为没有逐字来源，但也不算是拍脑袋编的"编造"，见来源与置信度）。

## 输入格式（stdin，`main()`）

```
PART 1
num_courses
num_prerequisites
a b            (重复 num_prerequisites 行；prerequisites[i] = [a, b])
```
或
```
PART 2
num_courses
num_relations
a b            (重复 num_relations 行；relations[i] = [a, b])
```

## 规则

### Part 1 — LC 210 原题，最小堆打破平局

英文原题（逐字引用）：

> There are a total of `numCourses` courses you have to take, labeled from `0` to
> `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]`
> indicates that you must take course `bi` first if you want to take course `ai`. Return the
> ordering of courses you should take to finish all courses. If there are many valid answers,
> return any of them. If it is impossible to finish all courses, return an empty array.

`part1(num_courses: int, prerequisites: list[list[int]]) -> list[int]`

课程编号 **0-indexed**（`0..num_courses-1`）。`prerequisites[i] = [a, b]` 表示 **a 需要先修 b**（跟
Part2 的方向刚好相反 —— 见下方 Part2 的说明，两个函数各自的 docstring 里都写清楚了，不会混）。

用 Kahn 算法做拓扑排序，但"当前可选课程集合"（入度为 0 的课程）用 **最小堆** 维护：每一步永远从所有
当前可选课程里挑 **编号最小** 的先修。这个 tie-break 规则是本题输出确定性、可测试的唯一原因 —— 不
遵守这个规则会导致输出和下面的样例对不上。如果存在环（无法修完所有课程），返回空列表 `[]`。

### Part 2 — 最少并行学期数（原创 follow-up，形状取自 LC1136 "Parallel Courses"）

`part2(num_courses: int, relations: list[list[int]]) -> int`

课程编号改为 **1-indexed**（`1..num_courses`），这是刻意沿用 LC1136 自己的编号习惯，跟 Part1 的
0-indexed **不一样** —— 两个函数签名不同、各自独立，只要各自文档写清楚就不会产生歧义。
`relations[i] = [a, b]` 表示 **a 必须先于 b 完成**（a -> b 的边；跟 Part1 "a 需要先修 b" 的方向刚好
相反，请注意）。

每个学期可以同时学习任意数量的课程，只要它们的先修课程都在**严格更早**的学期完成。返回修完所有课程
所需的最少学期数 —— 这就是这个 DAG 按 BFS 分层（Kahn 算法逐层处理）所需要的层数。如果存在环导致无法
修完所有课程，返回 `-1`。

## 样例

### Part 1（用最小堆 tie-break 手工验证过，必须精确匹配）

```
num_courses=2, prerequisites=[[1,0]]
-> [0, 1]

num_courses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]
-> [0, 1, 2, 3]
   (追踪：course0 入度0，先处理。这解锁 course1,2（入度都变0）-> 堆里是 {1,2}，弹出最小=1，处理 ->
   course3 入度减到1（还差 course2）。堆里剩 {2}，弹出2，处理 -> course3 入度减到0。堆里 {3}，弹出3。
   最终 [0,1,2,3]。)

num_courses=2, prerequisites=[[1,0],[0,1]]
-> []   (环)
```

### Part 2（手算验证过）

```
num_courses=4, relations=[[1,2],[1,3],[2,4],[3,4]]
-> 3   (学期1: {1}；学期2: {2,3}；学期3: {4} -> 共3学期)

num_courses=2, relations=[[1,2],[2,1]]
-> -1  (环)

num_courses=3, relations=[]
-> 1   (无依赖，3门课都能在学期1并行修完)
```

## 隐藏测试边界清单

- `num_courses=0`（两个 part 都应该优雅返回：`[]` / `0`，注意 `0` 门课等价于"0 个学期就修完"，不是
  `-1`）
- 单门课、无先修
- 长链（n 门课，每门依赖上一门）—— Part1 下无论 tie-break 规则如何这都会强制唯一顺序；Part2 下这会
  产生 n 个学期；用来做 perf 测试（约 1e4-1e5 门课，图类问题不适合按 1e5-1e6 的通用尺度来，理由见
  REPORT.md 复杂度部分）
- 多个不连通的分量（独立的链平行存在）
- 自环 `[[0,0]]`（课程依赖自己 -> 环，Part1/Part2 都应该识别出来并分别返回 `[]` / `-1`）
- Part1 中多门课同时入度归零时，必须严格按最小编号出堆（不能只用任意合法拓扑序蒙混过关）
- Part2 中 `relations=[]` 但 `num_courses>0` 时，答案恒为 `1`

## 变体

- 只返回是否可以修完所有课程（LC 207 "Course Schedule" 的布尔版本，是本题的子集）。
- Part2 变体：course 编号改为 0-indexed 但保持 "a -> b" 语义（换皮，不改算法）。
- 部分公司把 Part1 的 tie-break 换成"按输入顺序里最早出现的可选课程优先"而非最小编号 —— 遇到这种变
  体要先确认 tie-break 规则再写代码。

## 来源与置信度

- Part 1：https://leetcode.com/problems/course-schedule-ii/ （LC 210，MED 难度，OA 题库原题复用，
  2023 Canada index item #14）—— **高置信度**，逐字复用。
- Part 2：题库里引用了 LC 1136 "Parallel Courses" / LC 2050 作为一道电面 follow-up 的方向说明（仅
  标题引用，没有找到逐字题面）—— 本题的 Part2 是按 LC1136 的题意精确形式化，**不标记为"编造"**，因为
  它直接扎根于题库给出的具名引用，只是没有逐字来源可核对。置信度：中（方向确定，具体测例是我自己手
  算验证的）。

## 考什么

skills: S05 图：拓扑排序 + BFS 分层 + 确定性 tie-break（最小堆/FIFO）· 环检测 · 边界处理（0 门课、
自环、不连通分量）· 整数索引一致性（0-indexed vs 1-indexed 两套约定不能混用）
