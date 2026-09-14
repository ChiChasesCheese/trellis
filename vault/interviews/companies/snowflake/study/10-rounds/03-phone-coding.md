# 03 · 技术电面 coding（60 min = 10 介绍 + 40 编码 + 10 反问）

> 本轮用到的通用能力（[[Code Core MOC|code-core]]）：[[round.reading]] · [[round.communication]] · [[round.ambiguity]] · [[model.event-stream]] · [[toolbox.heap]] · [[toolbox.prefix-trees]] · [[algorithms.sliding-window]] · [[algorithms.shortest-path]] · [[verification.tests]] · [[transfer.snowflake]] <!-- code-core-links -->

> 本轮全部题目（含 GitHub 蒸馏补充的新题，按 28 法则排序）：[`../../CONTENTS.md`](../../CONTENTS.md) §03_phone_coding。本文件里点名的题是示例，不是全集。

> 事实层（形式 / 通过线 / 挂点来源）在 `../../loop/LOOP_GUIDE.md` §4，本章不重复。
> 本章回答：**明天坐下来练这一轮，具体做什么。**

## 这轮到底考什么（一句话）

**LC medium 的正确性 + 接住一个更难的 follow-up。** 和 Stripe 电面不同，这里不是"把业务白话翻成好代码"，是算法 + 类设计；和纯 LeetCode 不同，follow-up 几乎必来（O(n)→O(1)、加并发、加反向查询、加持久化）。

一手证据的两极：
- "coding wasn't LC style but something random"（Blind 2022）
- "They gave me leetcode hard on the screens"（Blind 2022）
- 早期职业一手（2026）："人都很好，会给 hint，帮 debug"

**实用读法：按 medium 练速度，按 hard 练 follow-up。** 两轮 back-to-back，第二轮可能是 SD——体力分配要留。

## 40 分钟怎么走

| 时间 | 做什么 | 出声说什么 |
|---|---|---|
| 0–3 | 复述 + 问约束（n 多大、有无环、tie-break、空输入） | "Let me restate… n up to 2·10⁵? Can the graph have cycles?" |
| 3–6 | 说 approach + 复杂度，**等面试官点头** | "I'll do a topological pass so each node's set is the union of its parents' — O(V+E) sets." |
| 6–8 | 写接口与 3 个自测用例 | "Here are the three cases I'll check: empty, single, diamond." |
| 8–25 | 实现 + 跑用例 | 边写边说"这里处理的是 X，边界是 Y" |
| 25–37 | follow-up | **先说思路再改代码**；时间不够就口述完整方案 |
| 37–40 | 复杂度复盘 + 还能优化哪里 | "The bottleneck is set unions; with bitsets it's …" |

**沉默面试官**：SD 轮有一手记录。coding 轮若也沉默，每 5 分钟自己说一句进度与下一步。

## 必做题（按 28 法则顺序）

| 顺序 | 题 | 为什么 | 命令 |
|---|---|---|---|
| 1 | **pc01 RBAC / DAG 权限继承**（4 part） | #1 题族（5 个来源）；Snowflake 自己的 ROLE/grant 就是 DAG；part 4 反向查询是挂点 | `python3 loop/mock.py start pc01 -m 40` |
| 2 | od02 In-Memory File System | 电面池 4 来源；做完口述线程安全版 | `mock.py start od02 -m 40` |
| 3 | pc03 Recent Event Stream | 滑窗 + 计数 + top，同族于 Stripe ps01 | `mock.py start pc03` |
| 4 | pc10 Distributed Tree Counting | 消息传递模拟；日志格式要逐字对 | `mock.py start pc10` |
| 5 | pc02 Closest Facility Grid | 多源 BFS；1000×1000 别用递归 | `mock.py start pc02` |
| 6 | pc04 Wiki Click Path | BFS + parent 表 + 字典序最小路径 | `mock.py start pc04` |
| 7 | pc05 Max Events II（LC 1751） | 2026-06 一手电面原题变体 | `mock.py start pc05` |
| 8 | pc06 Happy Number → Floyd | 一手：先 O(n) 再被要求 O(1) | `mock.py start pc06 -m 20` |
| 9 | od03 Transactional KV / od04 Rate Limiter | 技术筛 / 电面池；并发追问 | `mock.py start od03` |

## 挂点 → 对策

| 挂点 | 对策 |
|---|---|
| RBAC 用逐节点 DFS 到根，2·10⁵ 超时 | 拓扑序一次传播；deny 单独一遍；反向查询建 `permission → holders` 倒排 |
| follow-up 来了从头重写 | 第一版就把"求集合"与"输出格式"分开；follow-up 只改前者 |
| Happy Number 被要求 O(1) 卡住 | Floyd：快慢指针在"下一个数"函数上跑，和链表判环同一招 |
| 多源 BFS 写成对每个 D 单独 BFS | 所有 B 同时入队，一次 BFS |
| 日志 / 输出格式差一个字符 | 格式化集中在一个函数；照 problem.md 的样例逐字比 |
| 前 15–20 min 被问项目讲超时 | S1 准备 3 min 版；讲完主动说 "happy to go deeper later, shall we start coding?" |

## 语言

Python。JD 里 Java 4/6、C++ 2/6，但电面无"用 Python 被扣分"的报道；OA 历史上限过 Java/C++，那是 OA 不是电面。

## 明天怎么练

```bash
cd vault/interviews/companies/snowflake
python3 loop/mock.py start pc01 -m 40     # 读完 4 个 part 再动手
python3 loop/mock.py test pc01 -k part1   # 锁 part 1
python3 loop/mock.py test pc01            # 全量
python3 loop/mock.py ref pc01             # 对照参考解
python3 loop/mock.py status               # 进度板
```

读题解：`../30-articles/`（先做后读）。
