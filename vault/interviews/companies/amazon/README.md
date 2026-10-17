# Amazon · SDE, AWS Data Services —— 从这里开始

西雅图现场 onsite，10/20–21，每一轮先 LP 再技术。这一页告诉你：每一轮怎么准备、每天先练什么、东西都在哪。
每一轮的细节和剩下几天的排期在 [[LOOP_GUIDE]]。

## 先记住四件事

- **编码几乎都是熟题加追问**：word ladder、task / course scheduling、LRU、group anagrams、sliding window maximum、LCA、
  除法求值、拓扑排序。准备的重点是追问：空间压到 O(k)、输入改成流式、不许排序。
- **OOD 是最确定会考的一轮**：先给一个很小的需求，再连加 5–6 条；每条新需求要能「加一个类或改一行」接住。
- **代码不会被运行**：在记事本里写，用一个具体输入手动走一遍——这一步要练。
- **每轮先问 10–30 分钟 LP**：留给技术的时间只有 30–45 分钟；故事要 60–90 秒讲完。

## 每天练什么、在哪练

| 轮 | Anki | Obsidian |
|---|---|---|
| OOD | `低层设计（LLD）::10 Amazon 专项`：按顺序学，标 low priority 的放最后 | 题解 `solution-amz-*`，分关练习 `design-amz-*` |
| 编码 | `LeetCode Tops::20 Amazon 高频 A 档` → `::22 Amazon 近一月原题` → `::23 Amazon 模式强化`；最近考过的老题：`tag:amazon-seen-2026-10` | `interviews/core/coding/amazon/`：模式讲义 `patterns/`、近期题 `recent/` |
| 系统设计 | — | [[sd-index]]（`interviews/core/system-design/amazon/`） |
| LP | — | [[amazon/lp/question_bank\|LP 题库]] · [[story_matrix]] · `lp/stories/` · [[amazon/lp/drill\|每日演练]] |
| GenAI | — | `lp/genai/` |

顺序建议：每天先做 OOD deck 的新卡，再复习编码，零碎时间读一篇系统设计；LP 故事每天口述两个。

## 最近一个月考到的题

**编码**

| 题 | 真正考什么 | 在哪练 |
|---|---|---|
| Word Ladder | 把「每次改一个字母」建成图做 BFS；用通配符模式建邻接 | A 档 |
| Task Scheduler、Course Schedule I / II | 冷却时间的贪心计数；依赖的拓扑排序与环检测 | A 档；OOD 的 DAG 执行器 |
| LRU Cache | 哈希表 + 双向链表做到 O(1)；读也会改顺序 | A 档；OOD 的可配置缓存 |
| Sliding Window Maximum | 单调队列为什么 O(n)；只能存 O(k) 时怎么办 | A 档 |
| Group Anagrams | 不许排序时用 26 个字母的计数当签名 | A 档 |
| Number of Islands II、逐行输入的矩阵 | 动态加陆地用并查集；存不下整个矩阵时只留两行 | deck 22 |
| LCA、组织架构最低共同上级 | 二叉树 / 多叉树的最近公共祖先；查询很多时预处理 | A 档；deck 22 |
| 除法求值 + 缓存 | 带权图 BFS；重复查询缓存，新增等式时怎么失效 | A 档；deck 22 |
| 连接词的 Trie 写法 | 字典树 + DFS 判断一个词能否由别的词拼成 | deck 22 |
| 棋子最少几步吃掉国王 | 棋盘最短路 = BFS，不同棋子只是邻居定义不同 | deck 22 |
| 迷宫 + 方向限制 | 状态要是（行, 列, 方向），不只是位置 | deck 22 |
| Bus Routes、Safe Walk、Task Scheduler II、Reconstruct Itinerary、Jump Game II 返回路径 | 换个图 BFS；0-1 BFS；记上次执行时间；欧拉路径；贪心 + 回溯路径 | deck 22 |
| 多粒度滑动窗口限流 | 按 IP / 用户分 key 的滑动窗口计数，内存有上界 | deck 22 |

**OOD**：火车票价 · 购物车折扣引擎 · 披萨订单 · Linux find · 应急事件发布订阅 · 可配置缓存 · 停车计费 · 快递柜 ·
机器人餐厅 · 文件监听器 · 增删查最近值 · DAG 执行器 —— 全在 deck 10。

**系统设计**：短链接 · Amazon Lockers · 配送中心库存 · 跨区域文件复制 · 疫苗预约 · AI Agent 安全事件平台 · 外部排序 ·
员工目录（DynamoDB 分区键）—— 全在 [[sd-index]]。

**LP**：最常被问的问题和该用哪个故事在 [[amazon/lp/question_bank|LP 题库]]；面试官会当场要求「换一个更重大的故事」，
所以每个 LP 至少准备两个故事。

## 流程

- SDE II：OA → 一小时店面（先技术、后 LP）→ 四轮背靠背 onsite（现场或视频）
- 新毕业生 OA：两道编码 + Work Simulation 情景判断 + Work Style 问卷，共 2.5–4 小时
- 面完 2–9 天出结果；被拒后的冷冻期可能是 6 个月到 1 年
