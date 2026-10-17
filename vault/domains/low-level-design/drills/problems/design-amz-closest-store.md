---
nodes: [amazon.amz-closest-store, python.data-model, oop.interfaces]
tags: [problem]
---
# Drill：增删查最近值（Add / Remove / Closest）

一个整数的多重集合：可以放入、拿走，可以问「集合里离 target 最近的数是哪个」。规模从几十个数到一百万个数。
这是 Amazon 电面报告里的一道小型 OOD 题，题目的难点不在算法而在三件事：最近值只可能是前驱和后继、存储要能随值域约束而更换、一次查询读两次要在同一个版本上。
（具体 API、平局和重复值为重建，向面试官确认。）

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：给一个排好序的列表，实现 `closest(target)`。想清楚两个边界：target 比所有数都小或都大；两个数一样近时取哪一个，并把规则做成构造参数而不是写死。
- 第 2 关（约 15 分钟）：加 `add` 与 `remove`，允许重复值。删除不存在的值怎么表达？失败时集合有没有被改动？空集合上查最近值怎么办？
- 第 3 关（约 15 分钟）：面试官说「所有的值都落在 [lo, hi] 里，数据量可能很大」。让存储可替换，实现一个值域有界的版本，并说清它与有序列表各自的复杂度。
- 第 4 关（选做）：多线程同时增删查；再加 `k_closest(target, k)`，重复值各算一个。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-closest-store/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-closest-store -q`。

**评分点**
- 开场问了平局、重复值、值域三个问题，并说得出每个答案改变设计的哪里（[[amz-closest-store-how-asked-and-three-questions]]）。
- 职责切分清楚：门面管校验、平局与锁，存储只回答 floor、ceiling、count（[[amz-closest-store-objects-and-their-jobs]]）。
- 能写出只比较前驱与后继的 `closest`，并处理两个边界（[[amz-closest-store-stage1-closest-with-bisect]]）。
- 说得出有序列表、树状数组、平衡树的代价，并用输入输出验证（[[amz-closest-store-data-structure-sorted-list-vs-fenwick]]）。
- 只在真有两个实现的地方开接缝，平局规则用枚举而不是策略类（[[amz-closest-store-seam-only-where-two-implementations]]）。
- 值域约束来了只新增一个类，不改门面（[[amz-closest-store-followup-range-constraint-fenwick]]）。
- 删除失败不改变状态，树状数组的计数不会变成负数（[[amz-closest-store-failure-path-remove-missing]]）。
- 一把锁罩住读前驱与读后继，说得出为什么 GIL 不够（[[amz-closest-store-concurrency-one-lock-two-reads]]）。
- 避开只比较一个候选的错误（[[amz-closest-store-common-mistake-one-candidate]]）。

**题解**：[[solution-amz-closest-store]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
