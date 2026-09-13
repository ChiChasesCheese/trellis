# 02 · HR / HM Round —— 面试手册 + 完美 Sr Eng 学习画像

> 两个用途:
> **(1) 面试手册** —— Stripe HR/HM(recruiter + hiring manager + behavioral)轮的逐题标准答案,同时是 Chi 今年 promotion review 的逐题素材。
> **(2) 学习画像** —— 一份「完美 Senior Engineer 的能力画像」。集百家之所成,把 Chi 所在生态(snowglobe/pricing/funding + 周边 repo)里**最精华的实现/架构/模式**挖出来当学习标杆,让 Chi 知道该「往哪里看齐」。**目的是带着这份画像去 repo 里学知识、看实现,不是简历审计。**
> 语言:中文,技术名词/代码标识符/表名/文件路径保留英文。

---

## 怎么用

1. **先读 `evidence-base.md`** —— 素材总纲:Chi 画像 + 9 个旗舰故事(S1~S9)+ Ziyang 协作框定。所有面试答案从这里取材。
2. **`interview-manual/`** —— 逐题答案手册。每题两版:**答案 A(影响导向,60-90 秒)** + **答案 B(技术深度,追问 how/why 时展开)**。
3. **`resume-evidence-map/`** —— 学习画像。每个技术主题:**Baseline**(Chi 已有的真实实现,起点)→ **★ 往哪里看齐**(跨 repo 挑出的最精华实现,学习标杆)→ **知识点体系** → **学习锚点** → **面试话术**。**从 baseline 到标杆之间的 gap,就是 Chi 的学习路径。**

---

## Part 1 · 逐题面试手册 `interview-manual/`

| 文件 | 覆盖 | 题数 |
|---|---|---|
| `dim1-2-tech-depth-impact.md` | 技术深度与复杂度 + 业务影响与规模 | Q1–Q8 |
| `dim3-5-leadership-ambiguity.md` | 技术领导力 + 处理模糊性与 Ownership | Q9–Q12, Q17–Q20 |
| `dim4-mentorship.md` | 带教与协作(Ziyang) | Q13–Q16 |
| `dim6-hr-behavioral.md` | HR 行为题(ready for promotion / 优势 / 规划 / 批评反馈) | Q21–Q24 |
| `stripe-fit.md` | Stripe 公司特定 + 纯 HR fit(Why Stripe / 自我介绍 / 弱点 / 反问 等) | 10 题 |

**旗舰故事速查**(细节见 `evidence-base.md`):
- **S1** AMEX GRRCN 端到端管线(Ruby→Snowflake 迁移,$138.6B/21.96M 笔)
- **S2** Quality-Check & Handshake 框架 + 自我修正 ADR(平台化信号)
- **S3/S4/S8/S9** ACH / AU-Amex / Terraform / DoorDash 四个 RCA(go-to person)
- **S5** Net Settlement Pricing(旗舰,$55B TPV / $450M-月 float,含 shadow-run 对账)
- **S6** Fee Anomaly Detector ROI gate(staff 级判断)
- **S7** snowglobe-tools(自发基建)

## Part 2 · 完美 Sr Eng 学习画像 `resume-evidence-map/`

四个主题,每份含 Baseline + 跨 repo 看齐标杆(每份 8-9 个)+ 知识点体系 + 面试话术:

| 文件 | 主题 | 看齐标杆亮点(往这看) |
|---|---|---|
| `01-amex-pipeline.md` | AMEX fee 计算 / 端到端 Snowflake 管线 | `SnowflakeBusinessDate` Java UDF 策略模式(跨语言边界+领域规则+API 治理三合一);AMEX interchange 计算 proc(依赖注入/容错/幂等/可观测四合一);`EXECUTE_QUALITY_CHECK` 通用 runner |
| `02-netsettle-migration.md` | Net Settlement + 迁移 + shadow-run + PostgreSQL | shadow-run day-level 对账 SQL 模板(13.7M行/0.224%);SETTLE 取数 proc(幂等 MERGE+handshake+逐户灰度);CDC backfill 三级时间兜底模板;pricing Postgres 核心 schema |
| `03-oncall-observability.md` | 生产可靠性 / on-call / 可观测性 | Datadog 数据驱动告警路由(config as contract in IaC);stream 告警在无强约束数仓里的 exactly-once;ACH UDF overload tracing 教材 |
| `04-intern-kafka-k8s-spark.md` | Kafka + Kubernetes + Spring + Spark | ProtobufConverter template-method + poison-message 隔离;`TransactionEventConsumer` 幂等计费三层防线;K8s Deployment × Connect tasks.max 两级并行度模型 |

---

## 校准点(带着这些去学,面试用真实数字)

调查中把简历技术点在生态里的真实位置查清了。这些**不是"该删的水分",而是学习坐标**——告诉你每个技术点的真实底座在哪、该往哪深挖:

- **业务量**:可辩护的硬数字是 **$138.6B / 21.96M 笔 Amex 交易**(Chi 2025 Impact Summary)。简历 $600B 若指全平台/年化口径,面试前自行确认口径。
- **PostgreSQL**:AMEX 管线核心在 Snowflake;PostgreSQL 是 pricing 服务的 OLTP 主库(96 表/526 migration)。学习重点 = OLTP/OLAP 分工 + Postgres↔Snowflake sync(见 `02`)。
- **Kafka + K8s**:真实事件流底座在 `kafka-snowflake-connector` + pricing consumer;`kafka-proxy` pod(SASL+TLS)就是 "Kafka proxies within Kubernetes"。学习重点 = Connect sink + converter + 两级并行度(见 `04`)。
- **Sentry**:确实在用(braintree.sentry.io runbook + PagerDuty/Sentry 告警 + connector config `SENTRY_DSN`,三处独立确认),是 DALM/ingestion 层错误追踪。Datadog + Sentry + 自建 Streamlit(`ptf_explorer.py`)是完整可观测性三件套(见 `03`)。
- **Airflow/Spark**:Spark Validators 真实存在(DTBTPRWIZ-39/53/54);批处理校验学习重点见 `04`。

`interview-manual/` 里的 `【预估：xxx】` / `【待 Chi 补充：xxx】` 占位符,是需要 Chi 用真实数字/细节替换的地方(尤其带教题的日常 1:1/pairing 细节)。
