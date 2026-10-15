# Story × LP 覆盖矩阵

> 15 个候选故事 × 16 条 LP。P = primary（可作主答案），S = secondary（支撑 / 换角度）。
> 数据源：`coverage.py` 里的 `MATRIX`（改了映射就改它，然后 `python3 lp/coverage.py` 重新生成，下面的输出区原样粘贴）。
> bar = senior（`../AGENT_RULES.md` "Bar: senior"）：下面「senior 门槛检查」专门标出只到 junior scope 的 LP。
> 故事编号：S1–S11 = `core/stories/`；R1–R3 = 简历里的项目（无故事笔记）；M1 = Answers Q13/Q16 的带教证据。

## 1. 脚本输出（`python3 lp/coverage.py`，2026-10-15）

```text
$ python3 lp/coverage.py
```

| Story | 1 CO | 2 OWN | 3 IS | 4 ARAL | 5 LBC | 6 HD | 7 IHS | 8 TB | 9 BFA | 10 FRU | 11 ET | 12 DD | 13 HB | 14 DR | 15 BE | 16 SSBR | P | S |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **S1** Amex settlement pipeline |  | P | S |  |  |  | S |  |  | S |  | S |  | P |  |  | 2 | 4 |
| **S2** Quality-check framework + ADR |  |  | P | S |  | S | P | S |  | P | P |  | S |  |  |  | 4 | 4 |
| **S3** ACH fee NULL incident RCA | S | P |  |  |  |  | P |  | S |  | S | P | P | S |  |  | 4 | 4 |
| **S4** AU Amex refund fee (data ends thread) | P | S |  | S |  |  |  |  |  |  | P | P | S |  |  |  | 3 | 3 |
| **S5** Net Settlement / interchange source switch | S | P | S | P |  |  | S | S | S | S |  | S |  | P |  |  | 3 | 7 |
| **S6** Anomaly detector go/no-go |  | P | S | P |  |  | S |  | S | S |  | P | P | S |  |  | 4 | 5 |
| **S7** Schema pool (zero-copy clones) |  | P | P |  | S |  |  | S | P | S |  |  |  |  |  |  | 3 | 3 |
| **S8** Terraform 7-minute RCA |  | S |  |  |  |  | S |  | P |  | S | P |  | S |  |  | 2 | 4 |
| **S9** Amex payout-delay incident | P | S |  |  |  |  | S |  |  |  | S | S | S | S |  |  | 1 | 6 |
| **S10** Refund-fee billing-terms retraction | S | S |  | P |  |  | S |  |  |  | P | P |  |  |  |  | 3 | 3 |
| **S11** Intern: Kafka/Spring/Spark |  |  |  |  | S |  | S |  |  |  |  | S |  | S |  |  | 0 | 4 |
| **R1** Quant-Stroller (personal project) |  | S | P | P | P |  | P | P |  |  |  | S |  | S |  |  | 5 | 3 |
| **R2** AI-native Ruby/Kotlin to Snowflake/Java migration |  |  | S |  | P |  | S |  | P |  |  |  |  | S |  |  | 2 | 3 |
| **R3** Aiki / AikiCard (consumer apps) | P | S | S |  | S |  |  |  |  |  |  |  |  | S |  |  | 1 | 4 |
| **M1** Onboarding doc + new-engineer mentoring |  | S |  |  |  | P | S |  |  |  | S |  |  |  | S |  | 1 | 4 |
| **Primary count** | 3 | 5 | 3 | 4 | 2 | 1 | 3 | 1 | 3 | 1 | 3 | 5 | 2 | 2 | 0 | 0 | | |
| **Secondary count** | 3 | 7 | 5 | 2 | 3 | 1 | 9 | 3 | 3 | 4 | 4 | 5 | 3 | 8 | 1 | 0 | | |

### Per-LP coverage (P = primary, S = secondary; `solid P` = primary from S1-S10 employer work only)

| # | LP | P | S | solid P (S1-S10) | best stories (P first) | status |
|---|---|---|---|---|---|---|
| 1 | Customer Obsession | 3 | 3 | 2 | S4, S9, R3 / S3, S5, S10 | ok |
| 2 | Ownership | 5 | 7 | 5 | S1, S3, S5, S6, S7 / S4, S8, S9, S10, R1, R3, M1 | ok |
| 3 | Invent and Simplify | 3 | 5 | 2 | S2, S7, R1 / S1, S5, S6, R2, R3 | ok |
| 4 | Are Right, A Lot | 4 | 2 | 3 | S5, S6, S10, R1 / S2, S4 | ok |
| 5 | Learn and Be Curious | 2 | 3 | 0 | R1, R2 / S7, S11, R3 | THIN (primary only from personal/resume) |
| 6 | Hire and Develop the Best | 1 | 1 | 0 | M1 / S2 | THIN (primary only from personal/resume) |
| 7 | Insist on the Highest Standards | 3 | 9 | 2 | S2, S3, R1 / S1, S5, S6, S8, S9, S10, S11, R2, M1 | ok |
| 8 | Think Big | 1 | 3 | 0 | R1 / S2, S5, S7 | THIN (primary only from personal/resume) |
| 9 | Bias for Action | 3 | 3 | 2 | S7, S8, R2 / S3, S5, S6 | ok |
| 10 | Frugality | 1 | 4 | 1 | S2 / S1, S5, S6, S7 | THIN (one solid primary) |
| 11 | Earn Trust | 3 | 4 | 3 | S2, S4, S10 / S3, S8, S9, M1 | ok |
| 12 | Dive Deep | 5 | 5 | 5 | S3, S4, S6, S8, S10 / S1, S5, S9, S11, R1 | ok |
| 13 | Have Backbone; Disagree and Commit | 2 | 3 | 2 | S3, S6 / S2, S4, S9 | ok |
| 14 | Deliver Results | 2 | 8 | 2 | S1, S5 / S3, S6, S8, S9, S11, R1, R2, R3 | ok |
| 15 | Strive to be Earth's Best Employer | 0 | 1 | 0 | M1 | GAP (secondary only) |
| 16 | Success and Scale Bring Broad Responsibility | 0 | 0 | 0 |  | GAP (no story) |

### Gaps / thin LPs

- LP5 Learn and Be Curious: THIN (primary only from personal/resume)
- LP6 Hire and Develop the Best: THIN (primary only from personal/resume)
- LP8 Think Big: THIN (primary only from personal/resume)
- LP10 Frugality: THIN (one solid primary)
- LP15 Strive to be Earth's Best Employer: GAP (secondary only)
- LP16 Success and Scale Bring Broad Responsibility: GAP (no story)

### Story load (how many LPs each story is primary for; >4 means over-reliance)

- R1 Quant-Stroller (personal project): P=5, S=3
- S2 Quality-check framework + ADR: P=4, S=4
- S3 ACH fee NULL incident RCA: P=4, S=4
- S6 Anomaly detector go/no-go: P=4, S=5
- S4 AU Amex refund fee (data ends thread): P=3, S=3
- S5 Net Settlement / interchange source switch: P=3, S=7
- S7 Schema pool (zero-copy clones): P=3, S=3
- S10 Refund-fee billing-terms retraction: P=3, S=3
- S1 Amex settlement pipeline: P=2, S=4
- S8 Terraform 7-minute RCA: P=2, S=4
- R2 AI-native Ruby/Kotlin to Snowflake/Java migration: P=2, S=3
- S9 Amex payout-delay incident: P=1, S=6
- R3 Aiki / AikiCard (consumer apps): P=1, S=4
- M1 Onboarding doc + new-engineer mentoring: P=1, S=4
- S11 Intern: Kafka/Spring/Spark: P=0, S=4

### Sole-primary risk (LP answerable by exactly one primary story)

- M1: sole primary for LP6 Hire and Develop the Best
- R1: sole primary for LP8 Think Big
- S2: sole primary for LP10 Frugality

Totals: 15 stories x 16 LPs; LPs with a solid employer-work primary: 11/16; LPs with any P: 14/16; LPs with zero story: 1


## 2. 读矩阵：先看这五件事

1. **employer 工作里有 solid primary 的 LP：11/16**（脚本最后一行）。没有 solid primary 的 5 条：LP5 Learn、LP6 Hire&Develop、LP8 Think Big、LP15、LP16。
2. **LP15 / LP16 零 primary**：不要硬凑故事，使用 `question_bank.md` 里的 fallback（坦白 + 最近的相邻例子）。
3. **LP10 Frugality、LP6、LP8 是 sole-primary**：一个故事被问砸（或被追问出不实）整个 LP 就没了 → 优先补第二个故事。
4. **R1/R2/R3/M1 的 primary 不是 employer 证据**：被 Bar Raiser 追问细节时，这几个故事现在**缺信息**（各文件的 `【待 Chi 补】` 合计见 §5）。
5. **每个故事 primary 不超过 4–5 条**（R1=5 是个人项目；S2/S3/S6 = 4）——Amazon 面试官会交叉比对，同一个故事不要在同一轮、同一面试官面前出现两次。

## 3. senior 门槛检查：哪些 LP 只到 junior scope，缺什么细节能抬上去

Senior 的五个维度：**ambiguity · 跨团队无权威影响 · 超出任务的 ownership · 机制（不是一次性英雄行为）· 数据权衡 / 拉高水平 / 与 senior 干系人 disagree-and-commit**。

| LP | 现状（谁在撑） | 为什么算 junior scope | 需要 Chi 补的细节（把它抬到 senior） |
|---|---|---|---|
| **13 Have Backbone; Disagree and Commit** | S3（顶住「把 ACH 加排除名单」）、S6（对惯性说不） | 两个都是「坚持我的判断」，**缺 disagree-and-commit 的后半**：「决定与我意见相左，我仍全力执行」，也缺与**更资深干系人**的分歧 | 【待 Chi 补：一次你的建议被否决（尤其是被 senior/经理否决）后，你如何全力执行并且让团队不受损？没有就如实写"我没有一个完整的故事"，并在 drill Day 1 优先从 S5（选 A/B 时有没有资深同事倾向 A）、S9（revert vs conditional）、S2 评审里挖。】 |
| **6 Hire and Develop the Best** | M1（唯一 P，证据有警告） | 只有「带新人定义契约 + onboarding doc」，**没有被带者的可见成长，没有 code-review 痕迹** | 【待 Chi 补：被带的工程师现在独立 own 了什么；onboarding doc 帮几个人上手；一次你给出具体设计意见、对方改了的例子；是否参与过面试/评级】 |
| **8 Think Big** | R1（个人项目）；S2/S5/S7 为 S | employer 工作里没有「我提出更大方向并让别人跟着走」的证据；R1 是个人 | 【待 Chi 补：S2 框架被几个团队/多少人使用；S7 工具被谁采用；有没有一次你把一个小任务重新定义成更大的平台，并说服别人投入】 |
| **5 Learn and Be Curious** | R1、R2（都不是 employer 故事或证据薄） | employer 的学习是隐含的（零拷贝克隆、stream 行为），没有「我不会 → 我系统地学 → 我用上并有结果」的完整弧线 | 【待 Chi 补：S11 实习起点与学习路径；S7 里为什么去研究零拷贝克隆/Deployments API；R1 学 DSR/PBO 的路径】 |
| **10 Frugality** | S2（sole-primary） | 容量论证是好的，但缺**真实成本数字**（算力、人周、存储），S6 的「不值得做 2–3 月」是定性 | 【待 Chi 补：S1 的 `STREAM_HAS_DATA` 省了多少 warehouse 时间/credits；S2 方案 D 避免了多少新基础设施；S7 克隆相对全量拷贝省多少】 |
| **9 Bias for Action** | S7（个人工具）、S8（一行修复 + 7 分钟）、R2（证据薄） | 速度是真的，但 scope 小：**缺在不确定、有风险的决定上"calculated risk"**（官方措辞） | 【待 Chi 补：S5 shipped dark 时，你在信息不全下决定上线的那一刻——风险是什么、可逆性怎么保证、谁反对；S8 事后那 2 个同形风险是否推动了修复】 |
| **1 Customer Obsession** | S4、S9（商户/PM）；R3 薄 | 客户信号是第二手（PM 转述、商户报告）；**缺"为客户牺牲短期目标"或"主动发现客户没说出来的问题"** | 【待 Chi 补：S4 AU 商户漏掉的退款费金额；S9 商户最终拿到钱的时间与你是否直接沟通；有没有一次你在没人要求时，因商户影响而升级处理优先级】 |
| **14 Deliver Results** | S1、S5 | 数字存在，但 **setback → rise to the occasion** 的弧线（官方措辞 "despite setbacks"）不清晰；S1 美元口径未对齐，简历 `$600B+` 有风险 | 【待 Chi 补：S1/S5 里一个具体的障碍（延期、依赖方出问题）以及你如何绕过；对齐 S1 美元口径】 |
| **15 / 16** | 无 | 无故事 | 【待 Chi 补：任何一次你为同事创造更安全/更包容的工作环境，或评估过行动对第三方/用户的副作用并因此改变做法的例子；S3 的"commit 之前考虑对商户的二阶影响"、S10 的"避免按错误谓词过度补偿商户"可作 re-angle 候选，但需要你确认真实动机】 |
| 2 / 3 / 4 / 7 / 11 / 12 | 多故事 | 已是 senior scope（机制 + 数据 + 自纠） | 仍需补每个故事的"influence"细节，见各 `stories/Sx_*.md` §Senior 升级点 |

## 4. 简历口径风险（Bar Raiser 的 Dive Deep 会咬住）

| 简历表述 | 内部笔记口径 | 风险 |
|---|---|---|
| "Led development of the American Express transaction-fee calculation system ... processing **$600B+** in annual transaction volume" | S1：~22M 笔（半年）、金额量级 ~$1.4B（笔记自己写"口播只说量级"） | **差 ~400 倍**。面试官让你推导 $600B 时无法支撑。【待 Chi 补：$600B 指的是什么范围，面试前把简历和口播统一】 |
| "Spearheaded Braintree's net settlement project ... estimated hundreds of millions in working-capital savings" | S5：epic owner of record 不是我；~$450M/月 float 是项目级数字 | "Spearheaded" 与 "I own the fee side" 不一致。BR 追问 baseline 时说不清 |
| "Led development" / "owning the full pipeline end-to-end" | S1 证据边界：不说 top committer / 615 commits | 保持 "~90 PRs, two largest changes" 口径 |

## 5. 待 Chi 补总量（脚本统计）

（`grep -o '【待 Chi 补' lp/stories/*.md | sort | uniq -c`，2026-10-15）

| 文件 | 【待 Chi 补】数 |
|---|---|
| `stories/M1_onboarding-and-mentoring.md` | 11 |
| `stories/R1_quant-stroller.md` | 14 |
| `stories/R2_ai-native-migration.md` | 15 |
| `stories/R3_aiki-consumer-apps.md` | 11 |
| `stories/S10_refund-fee-retraction.md` | 5 |
| `stories/S11_intern-event-streaming.md` | 5 |
| `stories/S1_amex-settlement-pipeline.md` | 9 |
| `stories/S2_quality-check-framework.md` | 5 |
| `stories/S3_ach-null-incident.md` | 4 |
| `stories/S4_au-amex-refund-fee.md` | 7 |
| `stories/S5_net-settlement-interchange.md` | 8 |
| `stories/S6_anomaly-detector-go-no-go.md` | 6 |
| `stories/S7_schema-pool.md` | 5 |
| `stories/S8_terraform-rca.md` | 5 |
| `stories/S9_amex-payout-delay-incident.md` | 6 |
| **合计（stories/）** | **116** |

## 6. 怎么用这张表

1. 听到 LP 问题 → 先看 §1 第三个表该 LP 的 `best stories (P first)`。
2. 选故事时避开你**这一轮已经讲过**的故事；用 S 级故事换角度（各 `stories/Sx_*.md` §4 有开场句）。
3. 8 个 LP 问题 / 4 轮，建议的「一轮一个主故事」分配见 `drill.md` Day 4 的 mock 排布。
