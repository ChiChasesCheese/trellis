# LP 5 天练习清单

- 目标：8 个 LP 问题 / 4 轮，都能在 **90 秒内开口**、**2 分钟内讲完**、经得住 **3 层追问**。bar = senior。
- 每天约 2.5–3 小时；每天结束在文末打卡里写：今天补掉了几个 【待补】。
- 配套：[[00_how_lp_works]]（规则）· [[question_bank]]（题）· [[story_matrix]]（覆盖）· `stories/`（稿）。

## 自检量表（每次录音或计时后过一遍）

- [ ] 第一句话点题 + 一句零术语的系统介绍，不超过 15 秒。
- [ ] 动作句主语是 I，I 占 80% 以上；团队贡献显式划线。
- [ ] 至少一个经得住追问的数字：基线和测量方式都答得出。
- [ ] 有一句「我否决的备选」；缺了就只是叙事，不是判断。
- [ ] 结果带代价或机制：现在流程里多了什么。
- [ ] 总长：90 秒版 60–90 秒；2 分钟版不超过 2:15。
- [ ] 至少一个 senior 信号：ambiguity / 无权威影响 / 超出任务 / 机制 / 数据权衡。

## Day 1 · 地基：事实对齐 + 补洞 + 最硬的 3 个故事

- [ ] 读 [[00_how_lp_works]]（30 分钟）。
- [ ] 对齐口径（30 分钟）：
  - 简历 "$600B+" vs 「Amex 结算管线」 的约 22M 笔；选一个能辩护的口径，必要时回 Snowflake 重查
  - "Spearheaded net settlement" 改口播 "I own the fee side of the interchange track"
- [ ] 补 【待补】（60 分钟，最高优先级）：
  - 【待补】「Amex 结算管线」：第二个按这套模式接入的人？设计评审里的反对意见？
  - 【待补】「ACH 费用 NULL 事故」：谁提的「加排除名单」、最后谁定？灰度阶段缺的费用是否补了？
  - 【待补】「Net Settlement 数据源切换」：选 B 时有没有资深同事倾向 A？谁批准放开 toggle？
  - 这三个补完，LP 2 / 7 / 9 / 12 / 13 / 14 的 senior 力度立刻提升。
- [ ] 录音 「Amex 结算管线」、「ACH 费用 NULL 事故」 的 90 秒版（30 分钟）：先读稿，再脱稿，对照量表。
- [ ] 睡前（3 分钟）：写下 8 条 LP 各自的「一句话我是谁」。

## Day 2 · 流利度：「Quality-check 框架」 / 「澳洲 Amex 退款费」 / 「Net Settlement 数据源切换」 / 「退款费 billing-terms 复盘」 + 追问

- [ ] 每个故事：90 秒版脱稿 ×2 → 2 分钟版 ×1 → 把追问逐条用嘴答（不看稿）。
- [ ] 追问扮演：找人（或让 Claude 扮 Bar Raiser，只给故事第一句）连续追问 3 层；禁止出现 "we"。
- [ ] LP13 补洞（45 分钟）：
  - 回想 「Net Settlement 数据源切换」 / 「Amex 出款延迟事故」 / 「Quality-check 框架」 评审里有没有「我的意见没被采纳，我仍执行」的瞬间
  - 写 5 行事实：谁、什么意见、结果、你做了什么
  - 没有就写「没有」，不编
- [ ] LP6 补洞（30 分钟）：
  - 【待补】「新人 onboarding 与带教」：被带者现在 own 什么
  - 【待补】「新人 onboarding 与带教」：onboarding doc 的受益者
  - 【待补】「新人 onboarding 与带教」：一次具体的设计意见 + 对方改了什么
- [ ] 抽 LP 4 / 11 / 12 的每道题，3 秒内说出「首选故事 + 第一句」。

## Day 3 · 全覆盖：「费用异常检测器 go/no-go」–「Amex 出款延迟事故」 + 换角度 + 薄 LP 的坦白句

- [ ] 「费用异常检测器 go/no-go」 / 「schema pool」 / 「Terraform 7 分钟 RCA」 / 「Amex 出款延迟事故」：90 秒版各 ×2；每个换两个 LP 的开场句再讲一遍。
- [ ] 换角度训练（45 分钟）：
  - 同一个故事（先 「ACH 费用 NULL 事故」，再 「Net Settlement 数据源切换」）连抽 4 个不同 LP 的题，每次从不同的决定点开讲
  - 讲到一半偏了：land it and pivot，不道歉重来
- [ ] 薄 LP 坦白句（45 分钟）：LP 5 / 6 / 8 / 10 / 15 / 16，把「没有合适故事时」的说法讲得自然，各不超过 40 秒；不心虚、不编。
- [ ] 数字卡（20 分钟）：抄一张「能口播的数字」，睡前默写。
- [ ] 「Quant-Stroller 研究平台」 / 「AI-native 迁移」 / 「Aiki 消费者 App」：只保留经得住追问的部分，其余放弃。

## Day 4 · 整场模拟（4 轮 × 2 个 LP）

- 排布（一轮一个主故事，轮内不重复）：

| 轮 | LP 题 A（故事） | LP 题 B（故事） | 备注 |
|---|---|---|---|
| 「Quant-Stroller 研究平台」 | Ownership（「Amex 结算管线」） | Dive Deep（「澳洲 Amex 退款费」） | 开局最稳 |
| 「AI-native 迁移」 | Insist on the Highest Standards（「Quality-check 框架」） | Bias for Action（「Terraform 7 分钟 RCA」） | |
| 「Aiki 消费者 App」 | Have Backbone（「费用异常检测器 go/no-go」） | Earn Trust（「退款费 billing-terms 复盘」） | 最危险：LP13 |
| R4（可能是 Bar Raiser） | Are Right, A Lot（「Net Settlement 数据源切换」） | Customer Obsession（「Amex 出款延迟事故」） | 任何一题都可能追到第 4 层 |

- [ ] 每轮 55 分钟：2 个 LP 题（各 8–10 分钟含追问）+ 你自己的 5 分钟反问；计时，不看稿。
- [ ] 每轮后立刻过量表，写 3 句反馈。
- [ ] 随机化：打乱 [[question_bank]] 里任意 8 题，不看首选栏，先自己选故事再对答案。
- [ ] 一次「我没有这个故事」演练（LP 15 或 16）：用坦白句讲，限时 40 秒。

## Day 5 · 行程日 · 轻量

- [ ] 早上 30 分钟：过数字卡和每个故事的开场一句。
- [ ] 路上或酒店：只做量表的第 1 项（开场句）和第 4 项（否决的备选）；不新增故事。
- [ ] 睡前不熬夜；目标是诚实、具体、有节奏，不是更多故事。

## 数字卡

| 故事 | 数字 | 注意 |
|---|---|---|
| 「Amex 结算管线」 | 约 22M 笔 Amex 交易（半年）· 18 个月 · 约 1,800 行最大单 PR · 十几个加固 PR | 美元口径未定；不说 $600B |
| 「Quality-check 框架」 | 约 1,500 行框架 · 8 个 subject area · 50 个坏商户 / 35,000 · 96.4% 检查一次通过 · 80 万 vs 240 万行 | ADR 状态是 Proposed |
| 「ACH 费用 NULL 事故」 | 约 196 商户 · 约 $11.3M/天 · 4 个 e2e 缺口 | 止血 PR 不是我的 |
| 「澳洲 Amex 退款费」 | 1,079,627 vs 0 · 157 商户 · 50 条回复 / 3 团队 | |
| 「Net Settlement 数据源切换」 | >99.9% · 0.07% · 13,737,670 vs 13,768,430 → +0.224% | 0.07% 不等于 0.224%；$55B / $450M 是项目级 |
| 「费用异常检测器 go/no-go」 | 6 vs 18,140 商户 · 760M 行峰值 · 2–3 个月 | 来自评估文档，口播用量级 |
| 「schema pool」 | 约 2 秒克隆 · 3 篇 ADR | 个人仓库 |
| 「Terraform 7 分钟 RCA」 | 7 分钟 · 79 / 42 · 2 个同形风险 | 不说 "only resource" |
| 「Amex 出款延迟事故」 | 约 $4M · T+7 · 三天关闭 · 三位 owner 之一 | |
| 「退款费 billing-terms 复盘」 | 196,274 → 21,923 行 · 61 → 30 商户 · $11,123 → $5,854.52 | |

## 绝对不说

- "top committer / 615 commits"；"no bugs, no accidents"；"唯一 owner of net settlement"；"merchant by merchant"；"两周"；"零回归"。
- "I backfilled"（「ACH 费用 NULL 事故」）；"only resource missing it"（「Terraform 7 分钟 RCA」）；"parsing UDTFs"（「Amex 结算管线」）；点名同事、商户、实习生。
- 编造 1:1、PR review 细节（「新人 onboarding 与带教」）；编造任何一个 【待补】 的数字。

## 打卡

| Day | 今天补掉的 【待补】 数 | 录音次数 | 最弱的 LP |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
