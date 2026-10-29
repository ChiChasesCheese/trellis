# 最后几天：周四晚到周一 14:00（PT）

周一 14:00 PT 是第一场技术面：约 60 分钟，开头 10–30 分钟问简历和支付领域，剩下的时间在 HackerRank 或 Lark 代码板上写 1–2 道题，没有现成的测试用例，要自己写、自己跑；也可能插一段后端基础（八股）。所以这几天的重心按顺序是：**编码（写完、自测、讲清最优解）> 项目深挖 > 后端基础 > 支付系统设计 > 类设计**。设计和类设计更可能出现在后面几轮，但这几天打下底子，后面的轮次只需要复习。每一块写了打开什么、做到什么程度就停。时间不够时从每天的最后一块往前砍，**编码和项目深挖不砍**。

## 总览

| 时间 | 块 | 时长 | 做什么 |
|---|---|---|---|
| 周四晚 | 0 | 20 min | 给招聘官发邮件 |
| 周四晚 | 1 | 40 min | 公司一页结论、职位说明对照 |
| 周四晚 | 2 | 1.5 h | 编码 A 档第一组：缓存与设计类 |
| 周五 | 3 | 3 h | 编码 A 档第二组 + 3 道限时自测 |
| 周五 | 4 | 1.5 h | 项目深挖：S1 的 3 分钟版和 30 分钟版 |
| 周五 | 5 | 2 h | 支付系统设计 SD01 |
| 周五 | 6 | 1 h | 八股：幂等与事务、MySQL |
| 周六 | 7 | 2 h | 编码 A 档第三组 + 2 道限时自测 |
| 周六 | 8 | 2 h | 类设计：钱包与幂等转账、费用计算器 |
| 周六 | 9 | 2 h | 系统设计 SD09、SD11，口述 SD01 |
| 周六 | 10 | 1.5 h | 故事：S3、S9、S5，填空 |
| 周日 | 11 | 1.5 h | 编码模拟：50 分钟两道 |
| 周日 | 12 | 2 h | 系统设计 SD10、SD12，消费金融五题 |
| 周日 | 13 | 1.5 h | 八股：Redis、消息队列、缓存、Java 并发 |
| 周日 | 14 | 1 h | 中文版故事、动机三问 |
| 周日 | 15 | 30 min | 晚上：一页结论、反问、周一清单 |
| 周一 | — | 到 11:00 | 热身，然后停 |

块与块之间休息 10 分钟。Anki 只在零碎时间刷：`LeetCode Tops::24 TikTok 字节高频 · 整题答案` 的 `01 A 档：最高频`，和 `支付系统核心` 的「正确性工程」「账务与资金」两个分支。

## 限时自测怎么做

每道限时题都按考场条件：

1. 在一个空目录里新建一个 `.py` 文件，关掉编辑器的补全和 AI。
2. 计时 25 分钟：先说澄清问题和思路（2 分钟），再写代码。
3. 在文件末尾写 `if __name__ == "__main__":`，下面 4–5 个 `assert`：正常例子、空输入、单个元素、重复值、边界值。用 `python3 文件名.py` 跑通。
4. 计时结束后，把代码提交到 LeetCode 确认，再对照整题答案的「追问」部分，把每个追问要改的那一行说出来。

写完却没有自己的测试，在这一轮等于没写完。

---

## 周四晚

### 块 0 · 给招聘官发邮件（20 min）

打开 [[06-questions-to-ask]]，A 节末尾的邮件模板，填上名字发出去。要问清：级别、要求按 2-2 面并包含设计轮、周一用什么平台、有没有 AI 辅助编码轮、具体做哪个产品和市场。越早发，周五越可能收到回复。

### 块 1 · 公司与岗位（40 min）

- [[01-company-brief]] 第 0 节「一页结论」（10 分钟）。
- [[02-role-and-team]] 第 1 节职位说明对照，读「你的证据」一列（20 分钟）。
- 用英文说一遍 60 秒自我介绍：PayPal Braintree，Amex 结算与费用管线，净额结算的 interchange 切换，值班（10 分钟）。

### 块 2 · 编码 A 档第一组：缓存与设计类（1.5 h）

周一最可能出的就是这一类：一个带几个操作的小类，然后加追问。每道读整题答案 10 分钟：识别信号、代码、复杂度、追问。

[[tlc-lru-cache-0-whole|LC 146 LRU 缓存]] → [[tlc-tt-lru-cache-ttl-0-whole|带 TTL 的 LRU]] → [[tlc-lfu-cache-0-whole|LC 460 LFU]] → [[tlc-tt-rate-limiter-implementation-0-whole|限流器]] → [[tlc-time-based-key-value-store-0-whole|LC 981 时间戳 KV]] → [[tlc-tt-kv-store-snapshot-restore-0-whole|KV 快照与恢复]]

最后 25 分钟：从空文件限时写一遍 LRU，带自己的 `assert`。写不出来就再读一遍答案，明早再写。**23:00 停。**

---

## 周五

### 块 3 · 编码 A 档第二组 + 限时自测（3 h）

先读整题答案（1.5 小时，每道约 8 分钟，只读识别信号、代码和追问）：

[[tlc-longest-substring-without-repeating-characters-0-whole|LC 3]] · [[tlc-find-all-anagrams-in-a-string-0-whole|LC 438]] · [[tlc-subarray-sum-equals-k-0-whole|LC 560]] · [[tlc-number-of-islands-0-whole|LC 200]] 及 [[tlc-tt-islands-follow-ups-0-whole|岛屿追问]] · [[tlc-course-schedule-0-whole|LC 207]] · [[tlc-course-schedule-ii-0-whole|LC 210]] · [[tlc-kth-largest-element-in-an-array-0-whole|LC 215]] · [[tlc-top-k-frequent-elements-0-whole|LC 347]] · [[tlc-merge-k-sorted-lists-0-whole|LC 23]] · [[tlc-merge-intervals-0-whole|LC 56]] · [[tlc-meeting-rooms-ii-0-whole|LC 253]]

LC 438 要说出「26 个计数的数组代替哈希表」这一步优化；LC 560 要说出为什么前缀和哈希表里要先放 `{0: 1}`。只给出能跑的解、说不出最优解的理由，会被判不通过。

然后 3 道限时自测（每道 25 分钟 + 5 分钟复盘）：LC 560、LC 210（输出一个可行顺序，有环返回空）、[[tlc-tt-basic-calculator-ladder-0-whole|计算器梯度题]]（先做无括号版）。

### 块 4 · 项目深挖：S1（1.5 h）

第一场技术面开头就会问项目，而且会追问支付领域的细节。打开 [[interviews/companies/tiktok/behavioral/deep_dive|项目深挖演练]] 的项目 A（[[S1 Amex 结算管线|S1]]）：

1. 合上页面，说一遍 3 分钟版：问题、你的设计、规模、一个坏过的地方、你怎么知道它是对的（20 分钟，手机录音）。
2. 逐个回答 A1–A13，每个先自己答，再对照（50 分钟）。重点：怎么保证不重复不丢、数据模型和键、生产里坏过什么、哪些是你做的。
3. 背清楚三组数字：一年数千万笔、数十亿美元；净额结算 13.7M 行、字段一致率 > 99.9%；约 $450M / 月的垫资（20 分钟）。

### 块 5 · 支付系统设计 SD01（2 h）

1. 读通用题解 [[solution-payment-system]]（30 分钟）。
2. 读 [[sd01-payment-system]] 全文（50 分钟），重点：幂等分三层、状态机加复式账本同一事务、超时是「未知」不是失败、对账兜底。
3. 合上页面，口述 8 分钟：从「用户点支付」到「钱进卖家余额」，每一步回答四个问题：这里崩溃会怎样、消息重复会怎样、消息丢了或迟到会怎样、这个键过热会怎样（20 分钟）。
4. 跑一遍 [[tiktok-sd-index]] 里「贯穿所有题的五个问题」（20 分钟）。领域词汇不熟的，查 [[05-payment-domain]]。

### 块 6 · 八股：幂等与事务、MySQL（1 h）

[[tiktok-idempotency-transactions]]（30 分钟）→ [[tiktok-mysql]] 的索引、隔离级别、MVCC 三节（30 分钟）。每个问题盖住答案，用一句话说出来；说不出的标记，周日再看。**22:30 停。**

---

## 周六

### 块 7 · 编码 A 档第三组 + 限时自测（2 h）

读整题答案（1 小时）：[[tlc-tt-currency-conversion-queries-0-whole|汇率换算查询]] · [[tlc-evaluate-division-0-whole|LC 399]] · [[tlc-tt-seller-task-scheduler-0-whole|卖家任务调度器]] · [[tlc-tt-removable-timestamp-task-scheduler-0-whole|可删除任务的调度器]] · [[tlc-tt-concurrency-limited-runner-0-whole|限并发的任务执行器]] · [[tlc-search-in-rotated-sorted-array-0-whole|LC 33]] · [[tlc-binary-tree-maximum-path-sum-0-whole|LC 124]]

然后 2 道限时自测：汇率换算查询（无解返回 -1，再追问精度）、带 TTL 的 LRU（从空文件写，不看答案）。

### 块 8 · 类设计：支付味道的三题（2 h）

类设计考的是把几种数据结构拼成一个类，让每个操作都够快、几份结构始终一致。本页对应的五道支付类设计题在 [[07-class-design]]。先读 [[domains/under-the-hood/map/compose.patterns|组合模式总览]]（15 分钟，对应 Anki `::26 工具里的数据结构与算法` 的 `12 数据结构组合` 分支）。然后三题，每题先读题目文章，再动手：

| 题 | 读 | 动手 | 核心 |
|---|---|---|---|
| 幂等转账与账本 | [[ood20-wallet]] | `digital-wallet` 套件 | 整数金额；只追加的分录；两个账户按固定顺序加锁；客户端幂等键，同一个键带不同参数要报冲突 |
| 费用 / 税费计算器 | [[ood03-checkout-discount]] · [[ood18-aws-billing]] | `amz-aws-billing` 套件 | 规则是可组合的策略；金额用整数分；只在最后舍入一次；重复上报的用量不能多收钱 |
| 按商户限流 | [[ood14-rate-limiter]] | `rate-limiter` 套件 | 每个 key 的状态隔离和回收；被拒时告诉调用方多久后再试 |

动手的方法：把题目目录复制到一个临时目录，在 `starter.py` 里写；先给自己写 3 个测试，再跑整套。

```bash
cp -r vault/domains/low-level-design/problems/digital-wallet /tmp/dw
cd /tmp/dw && IMPL=starter uv run --with pytest python -m pytest -q
```

每题 35 分钟，做不完就停，对照 `solution.py` 看差在哪。

### 块 9 · 系统设计 SD09、SD11，口述 SD01（2 h）

- [[sd09-wallet-ledger]]（40 分钟）：充值通知重复只入账一次、热点账户、余额冻结、怎么证明账没被改。
- [[sd11-reconciliation-system]]（40 分钟）：内部账本、PSP 报告、银行流水三方对账；差异分类和调整分录。这是你在 PayPal 做过的事，准备好把 S1 接进来。
- 计时 45 分钟，对着空白页口述 SD01 全程，按 [[tiktok-sd-index]] 的「时间预算」走，录音（40 分钟）。

### 块 10 · 故事（1.5 h）

- [[S3 ACH 费用 NULL 传播事故|S3]]（值班、线上定位）和 [[S9 Amex 出款延迟事故|S9]]（多 owner 事故、SLA 定论）：各说 60 秒版和 2 分钟版（30 分钟）。
- [[interviews/companies/tiktok/behavioral/deep_dive|项目深挖演练]] 的项目 B（[[S5 Interchange 数据源切换|S5]]）：B1–B5（30 分钟）。
- [[interviews/companies/tiktok/behavioral/question_bank|行为题库]]：把所有【待补】填上，尤其是和 PM 的冲突、为什么离开 PayPal、为什么 Global Payment（30 分钟）。

---

## 周日

### 块 11 · 编码模拟（1.5 h）

按考场条件做一次完整模拟：50 分钟连做两道没做过的 A 档 medium，边写边说英文，每道都写自己的测试。做完复盘 30 分钟：哪里卡住、哪句话没说出来、复杂度有没有主动讲。可以从 [[interviews/core/leetcode/tiktok/README|A 档总表]] 里挑没读过的题。

### 块 12 · 系统设计 SD10、SD12，消费金融五题（2 h）

- [[sd10-creator-payouts]]（35 分钟）：余额分层、绝不重复打款、几天后才到的退票。
- [[sd12-payment-routing]]（35 分钟）：多 PSP 路由、有定论才切换、超时先查询。
- [[05-payment-domain]] 第 7 节，再读 [[02-role-and-team]] 第 2 节的五个话题：贷款生命周期、计提、授信、换汇舍入、跨区域容灾。每个读完合上，用 2 分钟说出来（50 分钟）。

### 块 13 · 八股（1.5 h）

[[tiktok-redis]] → [[tiktok-message-queues]] → [[tiktok-cache-problems]] → [[tiktok-runtime-concurrency]] 的 Java 部分（ConcurrentHashMap、线程池、GC）。每页只做末尾的速记表自测，说不出的回到对应问题。最后 10 分钟回看周五标记过的幂等和 MySQL 问题。

### 块 14 · 中文版与动机（1 h）

- 面试官在亚洲时常用中文开场，每轮可以选语言。S1 和 S3 各准备一个 90 秒中文口述（30 分钟）。
- 三个动机问题各说一遍，中英各一次：为什么 Global Payment、为什么离开 PayPal、能不能接受晚间会议和每周 5 天到岗（20 分钟）。
- [[interviews/companies/tiktok/behavioral/bytestyle|ByteStyle]] 的对照表扫一遍（10 分钟）。

### 块 15 · 晚上（30 min）

- [[01-company-brief]] 第 0 节（5 分钟）。
- [[06-questions-to-ask]] 里挑 3 个问题写在纸上：一个问值班或上线，一个问新市场，一个问 2-1 和 2-2 的区别（10 分钟）。
- 检查周一清单（10 分钟）。早点睡。

---

## 周一（到 14:00）

| 时间 | 做什么 |
|---|---|
| 09:00–10:00 | 热身：从空文件写一遍 LRU，带 `assert`，限时 15 分钟；再把 A 档第一组的追问各说一句 |
| 10:00–10:30 | 60 秒自我介绍、S1 的 3 分钟版，各说一遍 |
| 10:30–11:00 | 扫一遍 [[sd01-payment-system]] 的评分要点 |
| 11:00 | **停止学习**，吃饭，走一走 |
| 13:15 | 检查：会议链接和代码板链接能打开；本机 Python 能跑；耳机、网络、充电器；水；纸笔 |
| 13:50 | 进会议 |

**这一小时里**：

- 简历问题超过 20 分钟时，主动说「Happy to go deeper later — shall we move to the coding part?」
- 写代码前先说澄清问题、暴力解和复杂度、再说最优解，然后才动手。
- 写完自己造 4–5 个用例跑一遍，主动说出时间和空间复杂度。
- 追问来了，说出「要改的是哪一行、哪个结构」，不推倒重写。
- 最后留 3 分钟反问，用纸上的问题。
