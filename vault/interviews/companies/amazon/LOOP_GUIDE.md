# Amazon onsite：每一轮考什么、怎么过

SDE · AWS Data Services，西雅图现场，10/20–21。每一轮约 1 小时：先 15–30 分钟行为题（LP），再 30–45 分钟技术。
技术部分是编码、OOD（低层设计）、或系统设计之一。所有代码都写在不能运行的编辑器里，靠你手动走测试用例。
按 senior 标准准备：讲清范围和影响、比较两种方案的取舍、主动补测试和边界。

## 每一轮

### 行为题（LP，每一轮都有）
- 每位面试官问 2–3 道；Bar Raiser 那一轮可能整轮都是 LP，一题接一题追问
- 最常被问：紧 deadline 交付 · 承担职责之外的事 · 和经理意见不合 · 收到负面反馈 · 深挖根因 · ownership · 最近学了什么 · **怎么用 GenAI**
- 过线标准：一个故事 60–90 秒讲完；数字说得出口；说「我」做了什么；追问时能讲出取舍和机制
- 去哪练：[[amazon/lp/question_bank|LP 题库]] → [[story_matrix]] → `lp/stories/` → [[amazon/lp/drill|每日演练]]

### GenAI（常在 HM 那一轮）
- 会问：你怎么用 GenAI · AI 出错（幻觉）时你怎么发现和处理 · 怎么验证 AI 写的代码 · 什么时候信它、什么时候不信
- 过线标准：有具体例子；说得出你的验证方法（测试、对照、自己重算）
- 去哪练：`lp/genai/` 四篇

### 编码（1–2 轮）
- 评分看三样，作为一个整体：数据结构与算法 · 代码可读可维护 · 解题过程（澄清、取舍、测试）
- 常见题型：二叉树 / LCA · Top-K / 堆 · 网格 BFS · 拓扑排序 · DP · 滑动窗口 · 二分答案 · 字符串解析 · 区间 · 单调栈 · 并查集 · Trie
- 过线标准：先说暴力解和复杂度，再优化；写完用一个小例子手动走一遍；能接住「输入改成流式」「放大 1000 倍」这类追问
- 去哪练：Anki `LeetCode Tops::20 Amazon 高频 A 档` → `::22 Amazon 近一月原题` → `::23 Amazon 模式强化`；讲义在 `interviews/core/coding/amazon/patterns/`

### OOD / 低层设计（几乎必有一轮）
- 形式：30–45 分钟写类、接口和核心方法，然后面试官一条一条加 5–6 条新需求
- 过线标准：每条新需求「加一个类或改一行」就能接住；命名清楚；钱用整数分；时间从外部注入；说得出线程安全怎么做
- 去哪练：Anki `低层设计（LLD）::10 Amazon 专项`，按卡片顺序；每题有题解 `solution-amz-*` 和分关练习 `design-amz-*`

### 系统设计（按 senior 准备；AWS 的面试官可能临场把 OOD 换成系统设计）
- 你简历里写到的东西（Kafka、Snowflake、复制、对账）会被深挖到内部机制
- AWS 数据方向常问：主库 + 只读副本 + 故障切换 · DynamoDB 分区键怎么选 · LSM 和 B-tree 的取舍 · 一致性哈希 · 读后写一致性
- 去哪练：[[sd-index]]，先读 [[00_ddia_refresh]] 和 [[00_how_to_run_the_round]]

## 面试前必须做

- 【待补：简历上的「$600B+ annual transaction volume」与能拿出证据的数字不一致——选定一句口径（见 [[story_matrix]] 待补），面试官手里是旧版简历，主动纠正】
- 【待补：Deliver Results / 紧 deadline 故事缺一个具体障碍和你怎么绕过去——这是最常被问的一类】
- 【待补：Disagree and Commit 缺「争论输了、照样全力执行」的故事】
- 每一轮开场先 60 秒 Tell me about yourself（[[amazon/lp/question_bank|LP 题库]] 末尾）

## 剩下几天

| 天 | LP | 编码 | OOD / 系统设计 |
|---|---|---|---|
| 10/17 | 补上面三个【待补】；按 [[story_matrix]] 练 6 条 | deck 22 新卡 + `tag:amazon-seen-2026-10` | deck 10 前 6 题 |
| 10/18 | 练 6 条 + GenAI 四题；录音听一遍 | deck 23 前 8 个模式 | deck 10 后 6 题；读 [[00_ddia_refresh]] |
| 10/19（飞西雅图） | 每条 LP 过一遍 60 秒版 | 只复习做错的卡 | [[sd01-url-shortener]]、[[sd02-amazon-lockers]] 各口述一遍 |
| 10/20 当天 | 早上把 5 个最常用故事各讲一遍 | 不碰新题 | 不碰新题 |
