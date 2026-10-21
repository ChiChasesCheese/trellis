# Quality-check 框架 + 商户级 ADR（平台化 / 自我纠错）

**I replaced hand-written validation tasks with a config-driven quality gate, then wrote the ADR that overturned the granularity of my own design.**

## 适用 LP

- 主：**Invent and Simplify**、**Insist on the Highest Standards**、**Earn Trust**、**Frugality**
- 副：Are Right A Lot、Have Backbone、Think Big、Hire and Develop

## 数字

- 框架 PR **~1,500 行**
- 铺开 **8 个 subject area**，各 200–800 行，我自己铺
- **~50 个**持续失败商户（~4%）挡住 **35,000** 个商户
- **96.4%** 的检查一次通过，所以只存失败行
- 极端每月 **~80 万行**失败行，对比每商户每次一行 = 每天 **240 万行**
- 方案 D 的先例：TRANSFERS 区域已跑 **16 个月**
- 状态口径必须背："The framework and eight rollouts are live; merchant-level readiness is designed, reviewed, and proven for one subject area, and the framework-wide rollout is sequenced behind the net-settlement ramp." 不说「已改成商户级」

## S / T / A / R / L

### S
- 团队有**几十张对账表**，每张都有自己**手写的校验 task**
- 每加一张表 = 写、评审、发布一个新 task

### T
- 让加检查变便宜
- 让 "is this data safe to read" 成为**硬条件**，而不是 Slack 约定

### A
- **配置表**：一行 = 哪个 subject area 跑哪个存储过程、什么 **SLA**（另有日期列、JSON 参数）
- **通用 executor**（`EXECUTE IMMEDIATE`）写标准化 PASS / FAIL / WARNING；**exception handler** 把崩溃变成 FAIL 行
- **状态行**翻成 **Completed** 并复制到 share 层，下游 **JOIN** 它
- 自己**铺开 8 个 subject area**：加检查 = 插一行
- 生产规模下发现**自己的缺陷**：就绪判断按表，~**50** 个坏商户挡住 **35,000**
- 写 **ADR**：四个方案 + 正确性论证 + 容量分析
- 否决 **VARIANT**（关谓词下推）、**flatten**（单元格大小上限）、**新表**（新基础设施）；选**汇总行 + 每商户失败行**，"**strictest wins**"

### R
- 框架 + **8 次铺开**在生产
- 商户级就绪：**designed, reviewed, proven in one subject area**
- 更大范围铺开排在 **net settlement 之后**，不说已上线

### L
- **粒度**是随规模要重新审视的设计参数
- 修自己的缺陷走正式的 **ADR**
- 设计任何 gate 先问：一个检查失败，**blast radius** 是谁

## 追问与回答

- **Why dynamic SQL, isn't that risky?**
  - 这是 config-driven 的代价；配置经 **migration** 控制，不是用户输入
  - 真风险是失去**静态检查**；缓解：**exception handler** + 结果表**健康检查**
- **Why a status table, not task dependencies?**
  - 下游在**不同库/账号**；`AFTER` 依赖不跨账号；**复制的状态行**是最低公约数
- **What is the correctness argument for merchant-level?**
  - **Strictest wins**：先判 `NOT EXISTS(表级失败)`，再判 `NOT EXISTS(商户级失败)`
  - 未改造的 procedure 退化成表级阻塞 = 今天的行为
- **Why not VARIANT?**
  - secure view 上逐行 UDF / VARIANT 解析**关闭谓词下推**
  - VARIANT **16 MB/cell** 上限（~98K 商户）；扁平行 + 等值 JOIN 保留剪枝
- **What's the actual status?**
  - 框架 + 8 次铺开在生产；商户级 proven in one area（TRANSFERS，16 个月）；全框架铺开排在 net settlement 之后
- **What did you learn?**
  - 粒度要随规模重审；修自己的缺陷走更正式的流程；先问爆炸半径

## 换个 LP 讲

- **Invent and Simplify**：加校验从 "write a task, review, deploy" 变成 "insert a row"；别把 ADR 状态说成已上线
- **Insist on the Highest Standards**：下游不读半验证数据，做成 join 条件；讲 trigger-status 握手和 strictest-wins
- **Earn Trust**：自己发现并写 ADR 批评自己的设计；四方案否决理由外化；别夸大成「大家夸我」
- **Frugality**：只存失败行，最坏每月 ~800K 行而不是每天 2.4M；复用现有结果表、零新基础设施
- **Are Right, A Lot**：把自己的抽象当别人的代码一样 disconfirm；strictest wins 的正确性论证
- **Have Backbone**：对自己设计的反对；被追问时诚实说这不是与他人的分歧
- **Think Big**：不是 feature，是别人往上接的平台；8 次铺开、下游消费
- **Hire and Develop**：标准通过框架/ADR/onboarding doc 传递；没有 code-review 痕迹，别声称

## 待补

- 【待补：ADR 评审里有没有人提出异议、你如何回应；没有就如实说「review 无实质异议」，不要编冲突】
- 【待补：除 Snowglobe 团队外有无其他团队接入】
- 【待补：除你之外谁添加过 config 行、几次？("someone else added a check by inserting a row without asking me" 是核心证据)】
- 【待补：ADR 主要评审是谁（职级、团队）、提了什么问题、你如何改了 ADR；是否有人最初反对「改自己刚铺开的框架」】
- 【待补：评审里有没有一条没被采纳但你仍执行的意见（disagree-and-commit）；没有就用 「费用异常检测器 go/no-go」/S3 做 Backbone】

<details><summary>逐字稿</summary>

> Our team had dozens of reconciliation tables, and every new one got its own hand-written validation task. I replaced that with a config-driven quality-check framework. One row in a config table says which stored procedure to run for which subject area, with what SLA. A generic executor builds the call, captures the result, and writes a normalized pass, fail or warning row, and an exception handler means one broken check never takes down the others. When every enabled check passes, a status row flips to `Completed` and replicates to a share layer where downstream teams `JOIN` on it. So "is this data safe to read" went from a Slack convention to a SQL condition.
>
> I rolled it out across eight subject areas myself — adding a check became inserting a row. Then I saw a flaw in my own design: readiness was per table, so roughly fifty bad merchants out of thirty-five thousand blocked everybody. I didn't patch it quietly. I wrote an ADR: four alternatives, a correctness argument, and a volume analysis. The direction is reviewed and proven in one subject area; the broader rollout is sequenced behind the net-settlement work.

</details>
