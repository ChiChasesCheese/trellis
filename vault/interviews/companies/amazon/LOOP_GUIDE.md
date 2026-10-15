# Amazon onsite 指南 —— SDE I · AWS Data Services（按 senior 标准准备）

> 证据都在 `catalog/raw/`：`official.md`（官方，记作 O）、`forums.md`（110 条 2025–2026 面经，记作 F，§ 是它的小节号）。
> `推断` = 本 kit 的判断。岗位是 SDE I，但 Chi 的要求是**永远按 senior 准备**，所以下面每一轮都写了「senior 档」该做到什么。

## 0. 这一场长什么样

| 项 | 事实 | 证据 |
|---|---|---|
| 轮数 | SDE I：3–4 轮，每轮约 1 小时；同一天 3 轮，中间休息 30 分钟，或者分两天；Bar Raiser 可能线上补面 | F §4.5 |
| 每轮结构 | **15–30 分钟 LP + 30–45 分钟技术**（编码或 LLD） | F §1, §4.5 |
| 常见组合 | 1–2 轮 DSA 编码、1 轮 LLD（官方叫 *Logical and Maintainable*）、1 轮 HM（常带 **GenAI 讨论** + 编码）、1 轮 Bar Raiser（以 LP 为主） | F §4.1, §4.5 |
| 系统设计 | SDE I：63 条面经里 43 条有 LLD/OOD，**0 条有分布式 HLD**；SDE II+：47 条里 44 条有 HLD | F §4.1 |
| 但要防 | AWS 的 loop 经常临场把 LLD 换成 HLD（LC6891316，JC-amz882）；你简历里写到的东西（Kafka、Snowflake、复制）会被深挖 | F §1 |
| 编码环境 | Livecode：**背后没有编译器**，代码不能运行，只能自己手动走测试用例 | `coding/amazon_bar.md` |
| 出结果 | 面完 2–9 天；在线拒信最快 48 小时 | F §5 |

## 1. LP（每一轮都有，最重要）

* 官方说法：「Each interviewer will typically ask two or three behavioral-based questions」（O §2）。Bar Raiser 那一轮可能 40 分钟问 13–14 道 LP（LC8293563）。
* 2025–2026 年被问得最多的题（F §4.2）：
  * 紧 deadline 交付（9 次）
  * 承担职责之外的工作（6 次）
  * 和经理意见不合（6 次）
  * 收到负面反馈（5 次）
  * Dive Deep 根因调查
  * Ownership
  * 最近学了什么新东西
  * **GenAI 使用（12 次，新出现的高频题）**
* 怎么准备：`lp/00_how_lp_works.md` → `lp/story_matrix.md`（覆盖率和缺口）→ `lp/stories/` → `lp/question_bank.md` → `lp/drill.md`。
* Senior 档要做到：讲清楚范围有多大、怎么影响你管不到的人、建立了什么**机制**、用数据做取舍。缺口和对应的补法在 matrix 里：最缺的是 Disagree and Commit（争论输了之后照样全力执行）、LP16、Earn Trust。
* ⚠️ **简历数字风险**：简历写「$600B+ annual transaction volume」，但 S1 笔记里查出来的是半年约 2200 万笔、约 $1.39B。Dive Deep 的追问一定会问到。onsite 之前必须统一口径。

## 2. GenAI fluency（2025 年起新增，常在 HM 轮）

* SDE I 面经里 16/63 条出现过（F §4.1）。原题有：「How do you use GenAI?」「a time AI hallucinated」「how do you verify an AI-generated solution」「when do you trust an LLM」（F §4.2）。
* JD 原文：「using GenAI tools to boost productivity」。
* 你的优势：trellis 本身就是证据。你用多 agent 编排做学习系统，并且定了「绝不接受 agent 自报完成，验收门要自己重跑，数字要用脚本重新推导，用变异测试检验测试本身」这些规则，能直接拿来讲。材料在 `lp/genai/`。

## 3. 编码（1–2 轮）

* 官方评分维度：「data structures and algorithms, logical and maintainable, and problem-solving」，三者作为一个整体来看（`coding/amazon_bar.md`）。
* 高频题型（F §4.3）：二叉树（遍历 / 路径 / LCA）、Top-K / 堆、网格 BFS、拓扑排序、DP、滑动窗口、二分答案、字符串解析、区间、Dijkstra、单调栈、并查集（汇率换算）、Word Ladder、Trie。
* 怎么准备：`coding/plan.md` 规定每天 2 题；`coding/patterns/` 是 11 个模式（另有 5 个在补）；每题后面的 senior 追问要能讲出来。
* Senior 档要做到：主动澄清需求，比较两种解法的取舍，代码按生产标准写并自带测试，追问放大 1000 倍或改成流式输入时能接得住。

## 4. LLD / OOD（SDE I 几乎必有一轮）

* 题目频率（F §4.4，SDE I + SDE II+ 合计）：
  * 文件搜索 / 过滤 API（Unix find）14
  * Amazon Locker 11
  * 计费 / 价格计算器 11
  * Rate limiter 10
  * 停车场 7
  * Logger 5
  * LRU / LFU 4
  * Pub/sub 4
  * 任务调度 3
* 形式：30–45 分钟写类、接口、核心方法，然后面试官会再加 5–6 条扩展需求。一个好的设计应该让「几乎每条只改一行」（LC8293563）。
* 怎么准备：`lld/route.md`。仓库里已有的 LLD 题库会被复用，缺的题会补上。

## 5. 系统设计（senior 档；SDE I 面经里没出现，但 AWS 会临场换题，而且 Chi 要求按 senior 准备）

* SDE II+ 常见题：news feed、酒店 / 票务预订、Uber、库存 / 防超卖、Netflix、聊天、设备配置同步、文件存储、监控（F §4.4）。
* AWS 数据方向的原题在 F §3.3：DB 组的「主库 + 只读副本 + 故障切换」、DynamoDB 分区键怎么选、LSM 和 B-tree 怎么取舍、一致性哈希、读后写一致性。
* 怎么准备：先读 `sd/00_ddia_refresh.md`（DDIA 要点，每个都对应到 AWS 服务）和 `sd/00_how_to_run_the_round.md`，然后做 `sd/problems/`（5 道 AWS 数据风格的新题）加 `sd/route.md`（领域题库里该做的题）。

## 6. 5 天怎么排（10/15–10/19，10/19 飞西雅图）

| 天 | LP | 编码 | 设计 |
|---|---|---|---|
| 10/15 | 读 00；补 S1 数字口径；补最关键的几处【待 Chi 补】 | plan 第 1 天 | — |
| 10/16 | 按 matrix 练 6 条 LP | 第 2 天 | LLD：文件搜索 + Locker |
| 10/17 | 练 6 条 LP + GenAI 故事 | 第 3 天 | LLD：计费 / rate limiter；读 DDIA 速成前半 |
| 10/18 | 补齐剩下的 LP，讲给别人听或录音 | 第 4 天 | DDIA 速成后半 + 1 道 AWS 数据题 |
| 10/19 | 每条 LP 过一遍 60 秒版 | 第 5 天 + 模拟面试 | 只复习，不碰新题 |

面试当天每一轮的开场：先用 60 秒做 Tell me about yourself（`lp/` 里有），然后进 LP。
