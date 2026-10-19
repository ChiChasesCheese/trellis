# Fee anomaly detector 的 go/no-go（判断力 · 说不 · 分阶段）

**I inherited a departing intern's ML detector that had only run in QA, and instead of momentum I wrote a go/no-go that split it into a safe SQL phase and a gated ML phase.**

## 适用 LP

- 主：**Are Right, A Lot**、**Dive Deep**、**Have Backbone**、**Ownership**
- 副：Frugality、Invent and Simplify、Bias for Action、Deliver Results、Insist on the Highest Standards

## 数字

- 数字来自我自己的评估文档，尚未从生产复核；口播用量级，并说明这一点
- QA **6 个合成商户** vs 生产 **18,140** 商户：说 "six synthetic merchants versus eighteen thousand"
- QA **8.3 亿行** vs 生产 **390 亿行**：说 "under a billion rows versus tens of billions"
- 峰值一天 **7.6 亿行**：说 "up to about 760 million rows on a peak day"
- **1,468** plan code；**15,293** (plan, description) 组合：说 "about fifteen thousand plan combinations"
- QA 前两个商户占 **97%** 的行
- Phase 2：**5–8 人周**编码；**2–3 个月**到生产可信
- **99.5%** 阈值 × 每天数亿行 = 每天**数百万条**告警
- 唯一不可再生的是分析师 **disposition 标注**，离职前导出

## S / T / A / R / L

### S
- 离职的**实习生**留下一个 ML **费用异常检测器**，只在 **QA** 跑过

### T
- 决定：继续做，还是**评估**；并决定什么必须在他离开后**留得住**

### A
- 写 **go/no-go 评估**，而不是继续做
- 对比 **QA vs 生产**：6 个合成商户 vs ~**18,000**；不到 10 亿行 vs **数百亿**；峰值 ~**760M**
- 看出逐行 **numpy** 推理在生产规模会**超时**，QA 永远暴露不了
- 区分**会随离职消失**的和**可重建**的；离职前导出分析师**标注**
- 分阶段：**Phase 1** 确定性规则，纯 **SQL**；**Phase 2** ML 重训 2–3 个月，在**gate** 之后
- **冻结** Slack 告警和 CI/CD 工作，直到 gate 说 go

### R
- 不可替代的**标注已保全**；便宜的防御层有清晰路径
- 数字来自我自己的评估，尚未在生产复核

### L
- 一个经理可审计的**书面 gate**
- 宁可停一个项目，也不上线一个**凌晨 3 点**呼叫团队的项目

## 追问与回答

- **Who asked you to make this assessment?**
  - 见待补
- **How did you decide Phase 2 was a no-go and not just "harder"?**
  - 大 warehouse 上推理**必然超时**；精确率**无 ground truth**；告警量**每天数百万条**；估算 **5–8 人周** + **2–3 月**
- **What was the pushback?**
  - 见待补
- **How do you know your numbers are right?**
  - 来自**我自己的评估文档**，尚未从生产复核；口播用量级，这是诚实边界
- **What happened after?**
  - Jira DTBTTFOUND-3254 … 3261（label `anomaly-detector`）已开；Phase 1 / gate 当前状态见待补
- **What would make you say go?**
  - **业务驱动明确** + **shadow 精确率**达到阈值；具体阈值见待补
- **Wasn't that wasted intern work?**
  - 代码 / terraform / 训练配方（**固定 seed**）都可重建；唯一不可再生的是**标注**，已导出
- **What did you give up?**
  - 我对一个看似快速的胜利说了**不**，推迟了可见产出

## 换个 LP 讲

- **Are Right, A Lot**：生产前就用生产现实检验项目；强调 QA vs 生产量级、风险排序、制度化 gate；别把评估数字当已验证事实
- **Dive Deep**：问题不在模型，在 QA 永远跑不到的 numpy 循环；逐行推理 vs set-based；分布（前两个商户占 97%）
- **Have Backbone**：所有人期待我做完上线，我写下为什么不该，并冻结工作；用文档而非情绪；不是 disagree-and-commit
- **Ownership**：做的人要走了，我决定什么必须留下；先救标注
- **Frugality**：业务驱动出现前，2–3 个月重训不值得；不按沉没成本排序；无成本数字，别编
- **Invent and Simplify**：确定性规则根本不需要 ML；Phase 1 纯 SQL
- **Bias for Action**：离职前把标注导出，这是单向门

## 待补

- 【待补：评估是你自己发起还是经理要求（影响 Ownership vs 被分配）】
- 【待补：有没有人希望照原计划上线、你怎么回应】
- 【待补：Phase 1 是否已排期/上线，gate 当前状态】
- 【待补：go 的具体 shadow 精确率阈值】
- 【待补：What I'd do differently】
- 【待补：评估结论怎么说服经理/stakeholder（会议还是文档），谁签字冻结】
- 【待补：和离职实习生的交接——是否给了反馈/带他导出标注（不点名，别夸大）】

<details><summary>逐字稿</summary>

> I inherited an ML fee-anomaly detector from an intern who was leaving. It had only ever run in QA. The easy path was to keep building. Instead I wrote a go/no-go assessment. QA had six synthetic merchants and under a billion rows; production is eighteen thousand merchants, around fifteen thousand plan combinations, and up to about 760 million rows on a peak day. The serving design was a per-row numpy forward pass, which would time out at that scale, and QA could never have shown it.
>
> I split the problem. What disappears when the intern leaves versus what's reproducible from code: only the analysts' labels were irreplaceable, so I got those exported before their last day. Then a phased plan. Phase one ships only the deterministic consistency rule — amount equals rate times quantity plus fixed — as pure SQL, which Snowflake handles at billions of rows. Phase two, retraining and a new serving design, is two to three months and sits behind an explicit go/no-go gate. I froze the Slack alerting and CI/CD work until the gate says go. I'd rather stop a project than ship one that pages the team at 3 a.m.

</details>
