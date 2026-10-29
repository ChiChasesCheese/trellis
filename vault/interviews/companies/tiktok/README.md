# ByteDance Global Payment · Software Engineer（FPS）—— 从这里开始

目标岗位是 ByteDance 的 Software Engineer, Financial Product and Solution - Global Payment（San Jose）：给海外市场做先买后付、消费信贷、保险和钱包的后端。面试是一串「过了才约下一场」的单轮淘汰：每场约 60 分钟，开头先拷问简历和支付领域，再在代码板上写题，代码要能跑，测试要你自己写。按 senior（2-2）的标准准备，并主动要求包含系统设计轮的 2-2 面试。雇主、部门、级别和薪酬在 [[01-company-brief]]，职位说明逐条对照在 [[02-role-and-team]]，每一轮的细节在 [[LOOP_GUIDE]]。

**下一轮**：技术面，**2026-11-02（周一）14:00 PT**，约 60 分钟：简历与支付领域 10–30 分钟，然后 1–2 道编码，可能插一段后端基础（八股）。
**到周一怎么排**：照着 [[00-last-days-roadmap]] 做，不用再做决定。

## 流程

1. 招聘官电话：背景、地点、级别、薪资预期。
2. 技术面：简历拷问 + 编码，在 HackerRank 或 Lark 代码板上，没有现成的测试用例。
3. 技术面：八股 + 编码，或支付系统设计。在亚洲的面试官更常问八股，可能排在美国晚上。
4. 2-2 的面试再加一到两轮设计（支付系统、类设计）和项目答辩；有的团队用 AI 辅助编码轮（自己的 IDE 加 AI，看能跑的代码和写完的测试）。
5. HM：项目、行为题，常加一道题或一个高层设计；HM 决定级别。
6. HR，有时加一场越级经理面；然后定级、组匹配、offer。

每轮通过后几小时到两天约下一轮；轮次可能在同一天临时加。

## 什么决定结果

- **支付领域对口**：简历拷问会把你的费用计算、结算、对账当成领域知识来问，这是你最大的优势。
- **写完、自测、讲清最优解**：测试全过但说不出最优解的理由，也会被拒。
- **钱的正确性**：设计题盯住一条流程追问崩溃、重复、超时、对账，答案要前后一致。
- **级别**：没有设计轮，结果通常封顶在 2-1。
- **HM 的行为题**：和 PM 的冲突、ownership 要讲清哪些是你的决定。

## 每天练什么、在哪练

| 轮 | Anki | Obsidian |
|---|---|---|
| 编码 | `LeetCode Tops::24 TikTok 字节高频 · 整题答案` 的 `01 A 档：最高频` | [[interviews/core/leetcode/tiktok/README\|A 档总表]] · [[interviews/core/leetcode/tiktok/map/patterns\|模式识别]] |
| 类设计 | `::26 工具里的数据结构与算法` 的 `12 数据结构组合` | [[07-class-design]] · [[ood20-wallet]] · [[ood18-aws-billing]] · [[ood03-checkout-discount]] |
| 支付系统设计 | `支付系统核心`：先「正确性工程」和「账务与资金」 | [[tiktok-sd-index]]：SD01 → SD09 → SD11 → SD10 → SD12 |
| 支付领域与消费金融 | `支付系统核心`：「跨境与换汇」 | [[05-payment-domain]] · [[02-role-and-team]] 第 2 节 |
| 八股 | — | [[tiktok-fundamentals]]：先幂等与事务、MySQL、Redis、消息队列 |
| 项目深挖与行为 | — | [[interviews/companies/tiktok/behavioral/deep_dive\|项目深挖]] · [[interviews/companies/tiktok/behavioral/question_bank\|行为题库]] · [[interviews/companies/tiktok/behavioral/bytestyle\|ByteStyle]] |
| 公司与反问 | — | [[01-company-brief]] · [[06-questions-to-ask]] |

每天：先写一道限时题（空文件、关补全、自己写 `assert`），再读一篇设计，零碎时间口述一个故事。

## 第一轮之前必须做

1. 给招聘官发邮件：级别、要求 2-2 加设计轮、周一的平台、有没有 AI 轮、做哪个产品和市场（模板在 [[06-questions-to-ask]]）。
2. S1 和 S5 各练出 3 分钟版和 30 分钟版，数字背清楚（[[interviews/companies/tiktok/behavioral/deep_dive|项目深挖]]）。
3. S1 和 S3 各准备一个 90 秒中文版：每一轮可以选语言。
4. 【待补：为什么 Global Payment、为什么不到两年离开 PayPal、工作许可、能否每周 5 天到岗，每个一句话】
5. 每道练习题都写自己的测试：周一没有人给你用例。
