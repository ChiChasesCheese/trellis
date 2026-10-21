# 故事 × 价值 覆盖矩阵

- 15 个故事（S1–S11 + R1–R3 + M1）× 15 个 Headlands 看重的价值。
- **P** = 可作主答案；**S** = 支撑 / 换角度；`*` = 有保留（见 caveat 表）。

| Story | 1 LOWEGO | 2 CURIOUS | 3 AUTON | 4 AUTOTEST | 5 PERF | 6 DSTORE | 7 LINUXNET | 8 BREADTH | 9 FASTITER | 10 MONITOR | 11 DATAANAL | 12 DEBUG | 13 XTEAM | 14 REVIEW | 15 LANG | P | S |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **S1** Amex settlement pipeline |  |  | P | S |  | S |  | S |  | P | S | S |  |  |  | 2 | 5 |
| **S2** Quality-check framework + ADR | P |  | S | P | S |  |  |  |  | S | S |  | S |  |  | 2 | 5 |
| **S3** ACH fee NULL incident RCA |  |  | S | P |  |  |  | P | S | P | S | P |  |  |  | 4 | 3 |
| **S4** AU Amex refund fee (data ends thread) | S |  | S |  |  |  |  |  |  |  | P | S | P |  |  | 2 | 3 |
| **S5** Interchange source cutover |  |  | S | P | S | S |  | S | P |  | S |  | S |  |  | 2 | 6 |
| **S6** Anomaly detector go/no-go | S |  | P |  | P* | S |  | S |  |  | P |  |  |  |  | 3 | 3 |
| **S7** Schema pool (zero-copy clones) |  | P | P* | S | S | S |  | P* | P |  |  |  |  |  |  | 4 | 3 |
| **S8** Terraform 7-minute RCA + repo scan | P | P |  |  |  |  |  |  | S |  |  | P | S |  |  | 3 | 2 |
| **S9** Amex payout-delay incident | S |  |  |  |  |  |  |  | S |  |  | S | P |  |  | 1 | 3 |
| **S10** Refund-fee retraction | P | S |  | S |  |  |  |  |  |  | P | S |  |  |  | 2 | 3 |
| **S11** Intern: Kafka / Spring / Spark |  | S |  |  | S | P* |  | S |  |  |  |  |  |  | S | 1 | 4 |
| **R1** Quant-Stroller (personal project) |  | P | P | P | S |  | S* | S |  |  | S |  |  |  |  | 3 | 4 |
| **R2** AI-native Ruby/Kotlin to Snowflake/Java |  |  | S | P |  |  |  |  | S |  |  |  |  |  | S | 1 | 3 |
| **R3** Aiki / AikiCard (consumer apps) |  | S | S |  |  |  |  |  | S |  |  |  |  |  |  | 0 | 3 |
| **M1** Onboarding doc + mentoring | S |  |  |  |  |  |  |  |  |  |  |  | S | P* |  | 1 | 2 |
| **Primary count** | 3 | 3 | 4 | 5 | 1 | 1 | 0 | 2 | 2 | 2 | 3 | 2 | 2 | 1 | 0 | | |
| **Secondary count** | 4 | 3 | 6 | 3 | 5 | 4 | 1 | 5 | 5 | 1 | 5 | 4 | 4 | 0 | 2 | | |

- `*` = caveat (see the caveat table).

### Per-value coverage (`solid P` = primary from employer work S1-S10 only)

| # | Value | P | S | solid P | best stories (P first) | status |
|---|---|---|---|---|---|---|
| 1 | Low ego, collaborative | 3 | 4 | 3 | S2, S8, S10 / S4, S6, S9, M1 | ok |
| 2 | Genuine curiosity | 3 | 3 | 2 | S7, S8, R1 / S10, S11, R3 | ok |
| 3 | Autonomy, independent ideas | 4 | 6 | 3 | S1, S6, S7, R1 / S2, S3, S4, S5, R2, R3 | ok |
| 4 | Fully automated, extensively tested | 5 | 3 | 3 | S2, S3, S5, R1, R2 / S1, S7, S10 | ok |
| 5 | Performance limits | 1 | 5 | 1 | S6 / S2, S5, S7, S11, R1 | THIN (every solid primary is caveated) |
| 6 | Distributed storage / compute farm | 1 | 4 | 0 | S11 / S1, S5, S6, S7 | THIN (primary only from intern / personal / resume) |
| 7 | Linux, networking, single machine | 0 | 1 | 0 | R1 | GAP (secondary only) |
| 8 | Good at everything, many layers | 2 | 5 | 2 | S3, S7 / S1, S5, S6, S11, R1 | THIN (one clean primary) |
| 9 | Fast iteration (weeks) | 2 | 5 | 2 | S5, S7 / S3, S8, S9, R2, R3 | ok |
| 10 | Monitoring, proactive detection | 2 | 1 | 2 | S1, S3 / S2 | ok |
| 11 | Data analysis for decisions | 3 | 5 | 3 | S4, S6, S10 / S1, S2, S3, S5, R1 | ok |
| 12 | Debugging, root cause | 2 | 4 | 2 | S3, S8 / S1, S4, S9, S10 | ok |
| 13 | Cross-team communication | 2 | 4 | 2 | S4, S9 / S2, S5, S8, M1 | ok |
| 14 | Code review, mentoring | 1 | 0 | 0 | M1 | THIN (primary only from intern / personal / resume) |
| 15 | Java / C++ language depth | 0 | 2 | 0 | S11, R2 | GAP (secondary only) |

### Gaps / thin values

- V5 Performance limits: THIN (every solid primary is caveated)
- V6 Distributed storage / compute farm: THIN (primary only from intern / personal / resume)
- V7 Linux, networking, single machine: GAP (secondary only)
- V8 Good at everything, many layers: THIN (one clean primary)
- V14 Code review, mentoring: THIN (primary only from intern / personal / resume)
- V15 Java / C++ language depth: GAP (secondary only)

### Caveat table

| Story | Value | Caveat |
|---|---|---|
| S6 | V5 PERF | capacity reasoning before anything shipped, not profiling a running system |
| S11 | V6 DSTORE | consumer / sink side only; never operated the cluster |
| M1 | V14 REVIEW | no code-review trail; contract and architecture review only |
| R1 | V7 LINUXNET | one resume line (self-hosted CI, 8-GPU server); no detail written down |
| S7 | V8 BREADTH | personal repository, not the team toolchain |
| S7 | V3 AUTON | personal repository, not the team toolchain |

### Story load (values each story is primary for; >4 means over-reliance)

- S3 ACH fee NULL incident RCA: P=4, S=3
- S7 Schema pool (zero-copy clones): P=4, S=3
- S6 Anomaly detector go/no-go: P=3, S=3
- S8 Terraform 7-minute RCA + repo scan: P=3, S=2
- R1 Quant-Stroller (personal project): P=3, S=4
- S1 Amex settlement pipeline: P=2, S=5
- S2 Quality-check framework + ADR: P=2, S=5
- S4 AU Amex refund fee (data ends thread): P=2, S=3
- S5 Interchange source cutover: P=2, S=6
- S10 Refund-fee retraction: P=2, S=3
- S9 Amex payout-delay incident: P=1, S=3
- S11 Intern: Kafka / Spring / Spark: P=1, S=4
- R2 AI-native Ruby/Kotlin to Snowflake/Java: P=1, S=3
- M1 Onboarding doc + mentoring: P=1, S=2
- R3 Aiki / AikiCard (consumer apps): P=0, S=3

### Sole-primary risk (value answerable by exactly one primary story)

- S6: sole primary for V5 Performance limits
- S11: sole primary for V6 Distributed storage / compute farm
- M1: sole primary for V14 Code review, mentoring

- Totals: 15 stories x 15 values; values with a clean employer-work primary: 10/15; values with any P: 13/15; values with zero story: 0


## 缺口与怎么办

| 价值 | 现状 | 面试里怎么说 |
|---|---|---|
| **V5 性能** | 唯一主答案 S6 是上线前的容量推理；S5 窗口化 `ON` 是设计推理；**没有测量过的故事** | 先说 "capacity reasoning, not profiling"，讲 S6/S5，再讲你会怎么剖析，问对方当前瓶颈。补 `stories/templates.md` T2 |
| **V6 分布式存储/计算** | 只有实习的消费侧（S11）和使用者视角（S1 streams、S7 不可变分区） | "I understand the model as a user; I haven't operated or designed one." |
| **V7 Linux/网络** | 空白 | "Strongest as a user of Kafka/gRPC/Snowflake; I'd measure where the time goes first." 若有真实经验：【待补：真实的 Linux / 网络经验，一句话】 |
| **V8 各层都懂** | 只有 S3 是干净主答案（S7 是个人仓库） | 用 S3 的"SQL 语义 → 函数重载 → MERGE"逐层下潜 |
| **V14 code review/带人** | 只有 M1，且无评审记录 | 只说契约/架构层面的评审；"I read every diff"；补 T3 |
| **V15 Java/C++ 语言深度** | 没有故事，靠语言题和诚实线 | 见题库 Q8、Q9、Q12 |

## 读法

- 听到问题，先判断落在哪个价值，再选首选故事；同一场不要把同一个故事讲两次。
- 过载：S3、S7 各是 4 个价值的主答案；S6 的性能和 S11 的分布式都是**有保留**的主答案。
- 唯一主答案的风险：V5 只靠 S6，V6 只靠 S11，V14 只靠 M1。
