# od06 Query Audit Log — report

## Summary
一个"pg_stat for Snowflake"式的审计日志类：记录每次查询访问了哪些表/列 → 按时间窗查询谁访问过
某个名字、以及哪些名字最近没人碰过。来源本身是一道开放式系统设计题（面试官全程沉默，按候选人
自己的结构评分），本题把它收敛成一个有精确契约、可自动判分的两段式练习。

## Sources & confidence
HIGH——逐字 LeetCode Discuss 一手记录（2024-02-14，与 LC 212 Word Search II 同场高级电面），
面试官原话（转述）明确给出三个能力点（"find columns/tables accessed in a time period"、
"what columns/tables have not been accessed in some time t"）。但候选人自己说明这是开放题、
没有固定 API——本题的具体方法签名、"名字统一当表/列处理"的简化、以及效率要求，都是本仓库为了让
它可测试而做的**收敛**，problem.md 在 API 契约一节明确写出这条简化，不代表面试官原话规定了这些
细节。

## Approach by part
1. 每个 `name`（表名或列名统一处理）维护一条按 `(ts, query_id)` 全序排列的记录列表，
   `record_access` 用 `bisect.insort` 找插入位置（不假设 `ts` 按调用顺序递增，允许乱序上报）。
   `accessed_in_range` 用两次 `bisect_left`（分别以 `(t_start, "")` 和 `(t_end+1, "")` 为界，
   利用空字符串必定小于任何非空 query_id 这个技巧定位精确边界）取切片，代价是
   O(log(该 name 记录数) + 命中数)，与其他 name 的记录数、总记录数都无关。
2. `unaccessed_since` 只需要一个 `name -> 最近访问时间` 的字典，`record_access` 时 O(1) 比较
   更新；查询时遍历这个字典（大小 = distinct name 数）。这是本题对"避免线性扫描"的实际定义：
   **不扫描访问记录本身**（记录总数可能远大于 name 种类数），但遍历 distinct name 集合是可以
   接受的——一个更精巧的"按 last-access 排序的辅助结构"最初设计成"只插入、懒惰失效"的有序列表，
   实测在"几乎每次访问都刷新某个 name 的 last-access"这种（其实很常见的）输入分布下会退化成
   插入次数≈总记录数、单次插入 O(结构大小) 的移位成本，整体逼近 O(n²)——这正是本题 perf 测试
   最初触发的一个真实教训（10 万条记录、10.4s 超时），已经在 problem.md 的效率要求与并发追问 3
   里写清楚，主实现改用更简单也更快的字典方案。

## Pitfalls hidden tests target
- `record_access` 从不去重，同一个 query_id/name/ts 重复记录会在 `accessed_in_range` 里出现
  多次
- 乱序上报：`ts` 不保证按调用顺序递增，`accessed_in_range` 的结果仍必须按 `(ts, query_id)`
  正确排序
- `unaccessed_since` 用严格 `<`，`ts==t` 不算"早于 t"；只统计"曾经被访问过"的名字
- `t_start > t_end` 返回空列表而不是抛异常
- "看似更优"的按 last-access 排序 + 只插入的辅助结构，在真实的"访问持续刷新最大值"分布下会
  退化到接近 O(n²)——这是本题从一次真实 perf 测试失败里提炼出的教训，写进了并发追问而不是
  默默改掉不提

## Complexity & measured cost
`accessed_in_range` O(log k + 命中数)（k = 该 name 的记录数）；`unaccessed_since` O(distinct
name 数)；`record_access` 均摊 O(k)（bisect.insort 的数组移位，k 是该 name 当前记录数，实践中
远小于总记录数）。10 万条记录（分布在 2000 个 name 上）+ 1 万次查询通过 `run_script` 实测 well
under 2s / 256MB。

## Test inventory
16 tests — part1: 9（含 1 io、1 fmt）· part2: 7（含 2 io、2 perf）；edge 9 · fmt 1 · io 3 ·
perf 2。

## Skills exercised
S09 类设计先定 API 契约（在开放题里主动收敛出可测试边界，而不是等一个不会说话的面试官给答案）·
S06（时间窗查询，与限流器/事件流题共享二分定位边界的思路）· D06 审计/治理：不可变、时间窗、
多租户（系统设计侧延伸，见 sd06）
