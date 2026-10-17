# Amazon 冲刺：最近一个月考了什么、怎么练

这一页回答三个问题：最近一个月 Amazon 的店面和 onsite 实际出了哪些题、它们背后考的是什么能力、离面试只剩几天时
按什么顺序练。OA 不在这里——OA 之后的每一轮才决定 offer。所有练习材料都已经放进 Anki 和 Obsidian，下面每一类都写了去哪练。

## 1. 先记住三件事

1. **coding 几乎全是熟题或熟题的小变形。** 这个月被点名的是 word ladder、task / course scheduling、LRU、group anagrams、
   sliding window maximum、LCA、除法求值（399）、连接词（472）、拓扑排序。原因很简单：Amazon 的 coding 轮要在 30–45 分钟里
   同时看你的思路、代码和沟通，面试官更愿意用一道熟题加两三个追问来区分人，而不是出一道你读题就要 10 分钟的新题。
   所以准备的重点不是多刷新题，而是**熟题的追问**：空间压到 O(k) 怎么办、输入改成流式怎么办、不许用排序怎么办。
2. **OOD（低层设计）是最确定会出现的一轮。** 这个月被点名的 OOD 有十道：火车票价、折扣引擎、快递柜、可配置缓存、
   停车计费、应急事件发布订阅、Linux find、机器人餐厅、文件监听器、增删查最近值。它们的共同点是：先给一个很小的需求，
   然后连续加 5–6 条新需求，看你的类结构能不能「加一个类、改一行」就接住。所以每道题都要练到能说出「这条新需求落在哪个类」。
3. **代码不会被运行，而且每轮先问 10–30 分钟行为题。** coding 和 OOD 都是在记事本里写、口头走查，不编译不执行。
   这意味着两件事：一是要练手写和手动推演（拿一个具体输入一步步走），二是时间比你以为的少——行为题之后只剩 30–45 分钟。

## 2. 去哪练

| 轮 | Anki | Obsidian |
|---|---|---|
| OOD / 低层设计 | `低层设计（LLD）::10 Amazon 专项（Amazon OOD）`，12 道题，卡片顺序就是学习顺序，从最简单的开始 | 每题一篇题解 `solution-amz-*` 和一份分关练习 `design-amz-*`，入口 [[低层设计（LLD） MOC]] |
| Coding（新题） | `LeetCode Tops::22 Amazon 近一月原题（2026-10）`，14 张整题卡 | `recent/coding/amz_*`，解法在 `coding/solutions/` |
| Coding（这个月又出现的老题） | `LeetCode Tops::20 Amazon 高频 A 档` 里搜 `tag:amazon-seen-2026-10`，15 道 | — |
| 系统设计 | — | [[sd-index]]，7 道题，每道一篇完整题解 |
| 行为面试（LP） | — | 下面第 5 节 → `lp/question_bank.md`、[[story_matrix]] |

剩下几天的建议顺序：每天先做 OOD deck 的新卡（它最确定会考），再做 coding 的 `amazon-seen-2026-10` 老题复习，最后用
零碎时间读一篇系统设计题解。行为面试的故事每天口述两个。

## 3. Coding：题目和它真正考的东西

| 题 | 真正考什么 | 去哪练 |
|---|---|---|
| Word Ladder（LC 127） | 把「每次改一个字母」建模成图上的 BFS；用通配符模式建邻接，避免两两比较 | A 档 |
| Task Scheduler（LC 621）、Course Schedule（LC 207 / 210） | 冷却时间的贪心计数；依赖关系的拓扑排序与环检测 | A 档；OOD 的 DAG 执行器 |
| LRU Cache（LC 146） | 哈希表加双向链表做到 O(1)；读操作也会改变顺序 | A 档；OOD 的可配置缓存 |
| Sliding Window Maximum（LC 239） | 单调队列为什么能 O(n)；追问只能存 O(k) 数据时的取舍 | A 档 |
| Group Anagrams（LC 49） | 不许排序时用 26 个字母的计数当签名 | A 档 |
| Number of Islands II（LC 305）与逐行输入的矩阵 | 动态加陆地时用并查集；数据一行一行来、存不下整个矩阵时只保留两行 | deck 22 |
| LCA（LC 235 / 236）与组织架构最低共同上级 | 二叉树 / 多叉树上的最近公共祖先；查询很多时预处理 | A 档；deck 22 |
| 除法求值（LC 399）加缓存 | 带权图的 BFS；同一查询反复出现时缓存结果，新增等式时缓存怎么失效 | A 档；deck 22 |
| 连接词（LC 472）的 Trie 写法 | 用字典树加深度优先搜索判断一个词能否由别的词拼成 | deck 22 |
| 棋子最少几步吃掉国王 | 棋盘最短路就是 BFS；棋子走法不同只是邻居的定义不同 | deck 22 |
| 迷宫（LC 490）加方向限制 | 当「怎么走」受方向约束时，状态必须是（行, 列, 方向）而不只是位置 | deck 22 |
| Top K Frequent（LC 347）、Ones and Zeroes（LC 474） | 计数加堆 / 桶排序；二维容量的背包 | A 档 |
| Bus Routes（815）、Safe Walk（3286）、Task Scheduler II（2365）、Reconstruct Itinerary（332）、Jump Game II 返回路径（45） | 换个图来 BFS；0-1 BFS；用哈希表记上次执行时间；欧拉路径；贪心加回溯出路径 | deck 22 |
| 多粒度滑动窗口限流 | 按 IP / 用户等不同粒度限流：一个 key 函数加滑动窗口计数，内存有上界 | deck 22 |

## 4. OOD 的学习顺序

按 deck 10 的顺序走，每道题都比上一道多一种能力：

1. **Amazon 的 OOD 轮怎么打**：45 分钟怎么分配，记事本代码怎么写得「可维护」，追加需求时怎么回答。
2. **增删查最近值**：最小的一道，练「先问清楚再选数据结构」——有序列表还是按值域分桶。
3. **火车票价**：前缀和算票价，周末封顶这种「规则」怎么插进来而不改主流程。
4. **购物车折扣引擎**：折扣规则做成可插拔的对象；钱用整数分避免浮点误差。
5. **Linux find**：过滤条件可以 AND / OR 组合，新增一种条件只加一个类。
6. **应急事件发布订阅**：一个订阅者出错不能拖累其他订阅者。
7. **可配置缓存**：淘汰策略和存储后端是两条独立变化的轴，用组合而不是继承。
8. **停车计费**：跨时段计费要按费率变化的时刻切段，时间由外部注入才能测试。
9. **快递柜（现场版）**：在题库快递柜的基础上，现场 45 分钟写到哪一步、会被追问什么。
10. **机器人餐厅**：机器人的状态机，忙闲调度，电量不足时怎么办。
11. **文件监听器**：用快照比对发现变化，回调线程与停止、去抖。
12. **DAG 执行器**：依赖安装顺序与环检测，找出一段有 bug 的拓扑排序代码里的问题，最后并行执行。

## 5. 行为面试：这个月被问到的问题

每个问题后面是建议先用的故事；理由是 [[story_matrix]] 里这个故事对这条 LP 是主答案。换故事前，先看它够不够 senior
——这个月有面试官当场说「这个阻碍不够重大，换一个」。

| 问题 | 考的 LP | 先用 |
|---|---|---|
| A time you made a decision with incomplete information | Are Right, A Lot / Bias for Action | S6、S5 |
| A time you disagreed with a teammate or your manager, and how you handled it | Have Backbone | S3、S6 |
| Taking a calculated risk：风险怎么量化、兜底方案是什么、结果如何、重来会不会改 | Bias for Action | S7、S6 |
| Influencing without authority：用了什么手段、被拒绝过几次、最后怎么落地 | Earn Trust | S2、S10 |
| A time you pushed back against a decision that negatively impacted your team | Have Backbone | S6、S3 |
| A system was failing intermittently while the obvious metrics looked fine — how did you find the root cause, how long did it take | Dive Deep | S3、S8 |
| A problem that required in-depth thought and analysis — how did you know you were focusing on the right things | Dive Deep / Are Right | S4、S10 |
| 你如何评估客户体验 | Customer Obsession | S4、S9 |
| 一个重大的、事先没预料到的阻碍 | Deliver Results | S1、S5 |
| 需要深入进去才找到问题点的一次经历 | Dive Deep | S3、S8 |
| You identified a customer pain point；a customer asked for a requirement that is not feasible | Customer Obsession / Earn Trust | S9、S10 |
| Work outside your comfort area；How would you validate code written by AI?；a time you failed；a trade-off between two competing priorities | Learn and Be Curious / GenAI / Ownership / Deliver Results | R2、`lp/genai/`、S3、S5 |
| 20 分钟简历深挖：技术栈为什么这么选、trade-off 是什么 | — | 简历上每一行都要能讲出选型理由 |

## 6. 流程上要知道的事

- SDE II 的流程是：OA → 一小时店面（先技术题、后行为题）→ 四轮背靠背 onsite，可以选现场或视频。
- 新毕业生的 OA 变长了：两道 coding、一段 Work Simulation 情景判断、一段 Work Style 问卷，全程 2.5–4 小时；SDE-2 的 OA
  里有一段 15–20 分钟的系统设计。
- 被拒后的冷冻期，有多个说法称从 6 个月变成了 1 年，没有官方证实。

## 来源

- 一亩三分地：2026-09-16..10-16 Amazon 标签下 39 帖与题库 29 条，逐条记录（帖子编号、日期、级别、轮次、可见内容、置信度）在
  [[1p3a_2026-10-16]]。几乎每帖的核心段落要积分高于 188 才能看到（抓取时账号 99 分），题目来自可见文字、楼下回复、站方摘要和
  题库条目名；看不到的部分在各题题解的末尾注明是补全的。积分够了可以回去补全。
- Hello Interview：同一窗口 27 条 Amazon 报告，记录在 [[hellointerview_2026-10-16]]。
- 第 1 节的三条结论分别来自：一位 SDE II 在 onsite 后写的「基本不会有非常规题目」；同一位的「都是 dry run，不用跑」；
  Hello Interview 停车场题面「syntactically correct, although it will not be executed」；以及多帖里「每轮先问行为题」的描述。
- 第 5 节的问题来自一亩三分地的 4 帖与 Hello Interview 的 3 条报告；故事映射是依据 [[story_matrix]] 做的推断。
- 第 6 节来自一亩三分地 2026-10-02 的一篇 6–9 月面经整理帖（61 篇）和一篇 SDE II 全套面经。
- 抓取方法：用登录后的浏览器调用两站的公开接口，2026-10-16。
