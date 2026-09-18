---
title: TS08 · 可观测性与 On-Call
aliases:
  - TS08
  - 可观测性与 On-Call
tags:
  - interview/stack
  - stack/observability
  - stack/production
stories: [S3, S4, S8, S9, S2]
---

# 08 · 可观测性与 On-Call（Observability & On-Call）

> 知识层（想更深时去哪）：[[System Design MOC|system-design]]：[[reliability.observability]] · [[reliability.slo]] · [[reliability.resilience.retries]] · [[reliability.resilience.containment]]；[[Kafka MOC|kafka]]：[[monitoring.lag-e2e]] · [[monitoring.metrics-and-slo]] <!-- domain-links -->
> 适用于：JD 上出现 observability / monitoring / on-call / SRE / incident response；被问"线上出问题你怎么查"、"你们怎么知道系统有问题"。
> 不适用于：SRE 专职岗位的深度（容量规划、混沌工程、错误预算驱动的发布决策）——见第 5 节。

---

## 0. 这个栈在 JD 里到底在问什么

**一、你被 on-call 叫醒过吗。** 分水岭问题。写过代码和背过 pager 是两种人：后者知道告警响的时候第一件事不是修，是判断影响面。

**二、你查问题是有方法还是靠猜。** 面试官想听的是一条可复述的路径——从现象到根因，每一步为什么这么走。"我看了下日志发现是 XX"不算方法。

**三、你能不能区分"系统活着"和"系统正确"。** 这是高阶问题，也是数据系统从业者的主场。服务挂了会有人尖叫，**数据算错了可以静悄悄错上三天** —— 知道这个区别，并且知道要为它建不同的机制，是这一栏最值钱的回答。

---

## 1. 来龙去脉

### 1.1 从监控到可观测性：一个真实的区别，不是营销词

**监控（monitoring）是问你预先想到的问题。** CPU 超过 80% 告警，错误率超过 1% 告警。前提是你事先知道该看什么——你在为**已知的失败模式**布点。

**可观测性（observability）是能回答你事先没想到的问题。** 这个概念借自控制论：一个系统的内部状态能否从它的外部输出推断出来。

这个区别不是文字游戏。分布式系统的失败模式组合爆炸，你不可能预先列全。真实的故障往往长这样：某个特定商户的某一类交易，在某个时区的夜间批处理窗口，因为上游一个字段偶尔为空而算错——**没有人会预先为这个场景建一个 dashboard**。

所以现代的做法是：与其预测所有问题，不如保证系统吐出足够丰富的信号，让你能在事后**任意切片**去追问。三类信号：

| | 是什么 | 擅长回答 | 代价 |
|---|---|---|---|
| **Metrics** | 随时间变化的数值，带维度标签 | "有没有异常"、"什么时候开始的" | 便宜，但基数（cardinality）会爆炸 |
| **Logs** | 离散的事件记录 | "具体发生了什么" | 贵，量大，难检索 |
| **Traces** | 一个请求穿过所有服务的路径 | "慢在哪一跳"、"谁调了谁" | 需要全链路埋点，采样率是取舍 |

**它们的分工是：metrics 告诉你有问题，traces 告诉你在哪一段，logs 告诉你具体是什么。** 只有 metrics 会让你知道出事却查不出原因；只有 logs 会让你淹死在数据里还不知道该捞哪一段。

### 1.2 SLI / SLO / 误差预算：把"稳定"变成一个可以算的数

"系统要稳定"不是一个工程目标，因为它无法证伪。SRE 那套把它变成三个可计算的东西：

- **SLI（指标）** —— 一个真实反映用户体验的数。"成功请求 / 总请求"，"P99 延迟"。关键是**从用户视角定义**：用户不关心你 CPU 多少，关心请求成不成功。
- **SLO（目标）** —— 给 SLI 定一个目标值。"99.9% 的请求在 300ms 内成功"。
- **误差预算** —— `100% - SLO`。99.9% 意味着一个月可以坏 43 分钟。

误差预算是这套体系里最聪明的设计，因为它**把稳定性和迭代速度的矛盾变成了一个共享的数字**：预算还有富余，就可以激进发布；预算烧光了，停下来修稳定性。这个规则让"要不要上这个功能"从一场辩论变成一次查表。

**为什么不追求 100%**：成本是指数上升的，而且用户感知不到——用户的网络本身就没有 99.99% 的可靠性。追求 100% 是把钱花在用户看不见的地方。

### 1.3 告警：少而准，比多而全难得多

告警的唯一标准是：**它响了，是不是必须有人现在起床。**

不满足这条的都不该是 pager 告警，该是工单或 dashboard。理由很实际：**告警疲劳会杀死整套体系**。一个值班的人每晚被叫醒五次，其中四次是噪音，那么第五次——真的那次——他也会下意识地按掉。

从这条推出几个实践：
- **按症状告警，不按原因告警。** "错误率上升"是症状，用户能感觉到；"某台机器 CPU 高"是原因，可能完全无害。原因型告警会随着架构变化不断变成噪音。
- **每条告警都要有 runbook。** 半夜被叫醒的人不该现场推理，应该有一份"看到这个，先检查这三件事"。
- **定期清理。** 从没响过的告警和天天响的告警都该删或改。

### 1.4 On-call 的实际流程

事故响应有一个稳定的顺序，而且**顺序本身就是经验**：

1. **判断影响面** —— 谁受影响、多少、在变好还是变坏。**这一步在修复之前**，因为它决定后面所有动作的紧迫度。
2. **止血** —— 恢复服务优先于查明原因。回滚、切流量、关开关。**根因可以明天查，用户不能等到明天。**
3. **根因** —— 止血之后再查。
4. **修复与复盘** —— 真修，然后写无责复盘（blameless postmortem），产出可跟踪的行动项。

新手最常见的错误是**跳过第 1 步直接进第 3 步**——一头扎进日志查根因，半小时后才发现影响面比想象大十倍，或者其实无关紧要。

**无责的含义**不是"没人有错"，而是"人会犯错是系统的输入条件"。一个只要有人手滑就会出事的系统，问题在系统。追责会让人隐瞒信息，而复盘的全部价值在于信息完整。

### 1.5 数据系统的可观测性：一个被普遍低估的差异

前面讲的都是在线服务的框架。**数据系统有一个根本不同，而这正是我最有话说的地方。**

在线服务的失败是**响亮**的：接口 500、延迟飙高、用户投诉。几分钟内就有人知道。

数据系统的失败是**安静**的。一条计费管道少算了某一类交易的费用，所有作业都是绿的——任务成功执行了、没有报错、延迟正常。**唯一的异常是某张表里少了一些本该存在的行，而没有任何常规监控会发现这件事。**

它可能错上几天几周，直到财务对账、或者客户投诉。

这意味着数据系统需要**在"服务活着"之外，额外建一层"数据正确"的监控**：

- **数据量监控** —— 今天的行数和昨天差太多就告警（最便宜、最有效的一条）
- **数据契约校验** —— 不该为空的字段空了、枚举出现了新值、外键指向不存在的行
- **业务不变量** —— "每笔成功交易必须有对应的费用记录"这类断言。**注意它检查的是"应该存在的东西存不存在"，这是普通监控完全覆盖不到的方向**
- **对账** —— 两条独立路径算出来的结果必须一致

最后一条是数据系统的终极防线，见 [[10-correctness-idempotency]]。

---

## 2. 在我们这套系统里它怎么用

这是一套金融数据系统，所以 1.5 描述的那层"数据正确性监控"不是锦上添花，是主线。

### 2.1 三套工具，分工明确

**Datadog** —— 指标、APM trace、JVM profiling、日志注入。在 `pricing/kubernetes/config.yaml.erb` 的 ConfigMap 里是一整组环境变量：

```
DD_JMXFETCH_ENABLED: "true"     DD_TRACE_AGENT_PORT: "30126"
DD_PROFILING_ENABLED: "true"    DD_LOGS_INJECTION: "true"
DD_TRACE_SAMPLE_RATE: "1"       DD_ENV: "<%= @environment %>"
```

snowglobe 侧还有专门的 agent 部署（`snowglobe/kubernetes/datadog_agent.yaml.erb` + 51KB 的 configmap）。

**Sentry** —— 应用异常追踪，DSN 在同一个 ConfigMap 里按环境切 project。

**Splunk** 和自建的 **Streamlit** 应用 —— 后者是团队为特定管道做的自助监控面板（`NON_AGG_AMEX_TASK_MONITOR`）。

值得注意的是**两套并存的分工**：Datadog 看系统和性能，Sentry 看应用异常。这两个不是重复建设——一个 JVM 应用的未捕获异常和它的 P99 延迟是两类问题，各自的工作流也不同。

### 2.2 可观测性被做成了强制约束

这是这套系统里最值得讲的工程决策：**snowglobe 的 health check 存储过程必须携带 Datadog observability 属性**：

```
on_call_priority          on_call_pagerduty_service
on_call_slack_channel     on_call_run_book
```

而且这些 health check 按规范 colocate 在各 component 下的 `health_checks/` 子目录里。

**为什么这是个好设计**：它把 1.3 里"每条告警都要有 runbook"从一个约定变成了一个**结构性要求**——你写不出没有 runbook 的告警，因为那个字段是必填的。同样地，`on_call_priority` 强制作者在写监控的当下就回答"这个响了要不要叫醒人"，而不是等到半夜。

**把纪律编码进结构，而不是靠 code review 提醒**，这和 [[03-snowflake-warehouse]] 里 Quality-Check 框架的思路是同一个：标准一旦进了框架就不依赖任何人记得。

### 2.3 Quality-Check 框架：数据正确性的自动化关卡

1.5 说的那层监控，在这套系统里是一个框架（详见 [[S2]]）：集中式 config 表驱动、通用 procedure 动态执行校验、`CLX_TRIGGER_STATUS_V1` 的 trigger-status 握手告诉下游"这块数据已验证可读"。

**握手机制是关键**。下游的取数 procedure 里有这样的条件：

```sql
JOIN CLX_TRIGGER_STATUS_V1 T1
  ON T1.SUBJECT_AREA = 'Settlement'
 AND T1.STATUS = 'Completed'
 AND T1.PLATFORM = 'North'
```

也就是说，**下游不读"还没被宣告就绪"的数据**。这把"数据质量"从一个事后检查变成了一个流程门禁——校验没过，下游根本不会消费，坏数据不会扩散。这比"算完之后发现错了再回滚"强一个量级。

### 2.4 真实事故：四个案例，四种不同的形状

**S3 · ACH fee-calc（2026-07-29，`#snowglobe`）—— 安静失败的教科书案例**

一条 PagerDuty 告警：`CHECK_TRANSACTION_HAS_BRAINTREE_FEES`。注意这条告警的名字——它检查的是**"每笔交易都该有对应的 Braintree fee 记录"这个业务不变量**，正是 1.5 里说的"应该存在的东西存不存在"。

根因链：Standard ACH（`ACH_FASTER_FUND` 关闭）promote 进 `TRANSACTIONS` 时 `payment_instrument_sub_kind` 为 NULL → 费用品类映射写的是 `'BT_' || NULL`，在 SQL 里等于 NULL → 匹配不到任何费率 → **不生成 discount/settled fee，且不报任何错**。最终定位到 `GET_EVENTSTREAM_PAYMENT_INSTRUMENT_SUB_KIND()` 的 1-arg 与 2-arg 重载歧义。

影响：约 **196 个 merchant、约 $11.3M/day GMV、约 105 万行**，98.9% 是 `us_bank_account`，100% 归因 `STANDARD_ACH`。

**这个案例把 1.5 讲的每一点都坐实了**：所有任务绿灯、没有异常、没有延迟告警，唯一的信号来自一条专门检查业务不变量的 health check。如果没有那条 check，这个错误会一直跑下去。

**S4 · AU Amex refund fees（2026-08-03，`#service-pricing`）—— 用数据终结分歧**

PM 走正式流程报 AU 商户的 Amex refund fee 疑似有问题，thread 拉了 50 多条，各方对是数据问题、配置问题还是逻辑问题意见不一。

处理方式是直接拉对比：**USA 1,079,627 行 vs AUS 0 行**，跨 157 个 merchant。根因是所有 AU merchant 的 `fee_refund_policy` 都是 `'partial'`、从来不是 `'full'`，导致 non-agg Amex refund fee 在 AU 根本不生成。

方法论上值得说的：**"零"是一个极强的信号**。一个数字偏低可能是正常波动，一个维度上恰好是 0 而另一个维度上是百万级，那基本只能是逻辑分支从未被走到。查这类问题先做维度对比，比读代码快得多。

**S8 · Terraform grant ownership（2026-08-13，`#treasury-services-releases`）—— 快速 unblock**

release 被 `GRANT OWNERSHIP` 失败卡住，约 7 分钟定位根因（`FEE_ANOMALIES_REVIEWER` 持有依赖的 USAGE grant，资源缺 `outbound_privileges`），出 PR #1326，release 部署成功。详见 [[04-terraform-iac]] §2.3。

**这里的关键不是快，是知道往哪看** —— 速度是领域熟悉度的副产品，不是天赋。面试里这么讲比讲"我 7 分钟就解决了"可信。

**S9 · DoorDash Amex 出款延迟（2026-07-06，事故频道）—— 边界澄清比修复更重要**

正式事故频道，被指定为三个 fix owner 之一。争议点是 SLA 到底违没违约，而我给出的判定是：**T+7 是我们美国境内管线的 SLA，但真正的约束是必须等 Amex 把钱 settle 到我们账户之后才能出款** —— 所以这不是管线违约，是上游资金到账时点决定的。

**事故里最贵的往往不是 bug，是各方对边界的误解。** 把边界讲清楚，争议自然消解。

### 2.5 我做的部分 `[me]`

上面四个事故我都是处理人或被指定的 owner 之一：[[S3]] 的根因是我给的并持续 owning 数周到 UDF 重载收口（DTBTTFOUND-3246）；[[S4]] 是被 PM 正式 escalate 后路由给我的；[[S8]] 是我出的 PR #1326；[[S9]] 是事故指挥点名的三个 fix owner 之一，SLA 问题上其他人 defer 给我。

Quality-Check 框架是我建的（PR **#1997，1,489 行**）并在约 8 个 fee subject area 铺开。**一个必须说清的边界**：我后来发现原框架有"某 subject area 约 4% 失败就 block 全部 merchant"的设计缺陷，写了正式 ADR 提出改成 merchant-level（Confluence `2894288991`，含正确性证明和 3 个被否方案）—— 但**那份 ADR 至今状态是 `Proposed`、`Date Approved: [pending]`，代码里的 `HAS_MERCHANT_DETAIL` 并不存在。也就是说方案提了，没落地。**讲这件事必须讲成"我识别出缺陷并写了提案"，不能讲成"我改好了"。

另外在 Slack 的 86 个频道里被团队按名 ping 做 go-to person —— 这个不是自封的，`slack.md` 里有 10 条具体实例，包括 George Fashho 在 SLA 问题上明说 "I would defer to Chi Zhang"。

原始证据：本机 `raw/slack`、本机 `raw/jira`、[[S2]]。

---

## 3. stripe kit 考到的点

OA 不考监控，但考**自测纪律**——那是同一种思维的小尺度版本：

- [[s18-validation-error-paths|S18 校验与错误路径]] —— 对应 health check 检查业务不变量
- [[s09-byte-exact-output-format|S09 字节级精确的输出格式]] —— 对应"安静失败"：输出多一个空格不会报错，只是全挂
- [[s11-idempotency-dedup|S11 幂等 / 去重]] —— 事故恢复时能不能安全重跑，取决于这个

`study/00-essentials/09-debug-and-selftest.md` 那篇讲的"每写完一个 part 立刻自测"，本质上就是 1.5 的那层数据正确性监控搬到 60 分钟的尺度里。

---

## 4. 常见追问与答法

| 追问 | 一句话答 | 展开的抓手 |
|---|---|---|
| 监控和可观测性的区别 | 监控回答你预先想到的问题，可观测性让你能追问事先没想到的 | 1.1，以及为什么分布式系统列不全失败模式 |
| 三支柱怎么分工 | metrics 告诉你有问题，traces 告诉你在哪段，logs 告诉你具体是什么 | 1.1 那张表 |
| SLO 怎么定 | 从用户视角定 SLI，误差预算把稳定与速度的矛盾变成一个共享数字 | 1.2；为什么不追求 100% |
| 告警太多怎么办 | 标准只有一条：响了是不是必须现在起床。按症状不按原因 | 1.3；告警疲劳会让真告警也被按掉 |
| on-call 拿到告警第一件事 | 判断影响面，不是查根因 | 1.4 的四步顺序 |
| **（三层）数据算错了但所有任务都是绿的,怎么发现** | **这是数据系统的核心难题。要额外建一层业务不变量断言,[[S3]] 那个 `CHECK_TRANSACTION_HAS_BRAINTREE_FEES` 就是** | 1.5 + 2.4 的 [[S3]]——**这是我最强的一个回答** |
| **（三层）怎么防止坏数据扩散到下游** | **trigger-status 握手:校验没过下游不读,把质量变成门禁而不是事后检查** | 2.3 的 `CLX_TRIGGER_STATUS_V1` |
| **（三层）你说的 go-to person,有没有反例** | **有。我通常是被指定的多个 owner 之一,不是唯一 owner** | 主动给出这个限定比被问出来强 |

---

## 5. 我的边界

**我不是 SRE，没做过容量规划和混沌工程。** 压测、容量模型、故障注入演练这些我没实操过。
→ 我会说："我的 on-call 是应用和数据管道层面的，不是平台层面。容量规划、混沌工程这些是专职 SRE 的活，我们团队依赖平台团队。"

**误差预算驱动发布决策，我们没真正跑起来。** 我理解这套机制，但我们团队没有到"预算烧光就停止发布"的成熟度。
→ 我会说："SLO 我们有，但没有严格用误差预算去 gate 发布。我知道那套怎么运作，但如果说我实践过，不老实。"

**在线服务的性能诊断不是我的强项。** JVM GC 停顿、连接池耗尽、线程死锁这些我没深入排查过。
→ 我会说："我的性能问题都在查询和管道层面——Snowflake 的剪枝、MERGE 的扫描范围、任务依赖链的延迟。服务端的延迟分位诊断我经验少。"
→ 接回去："不过定位方法论是通的：先确认影响面和边界，再用维度对比缩小范围，再进代码。AU Amex 那次用 USA 一百万行对 AUS 零行把范围一次性锁死，用的就是这个路子。"

---

## 6. 往深里看

| 节点 | 什么时候去读它 |
|---|---|
| [[reliability.observability]] | 三支柱的完整体系、埋点策略、采样 |
| [[reliability.slo]] | SLI/SLO/误差预算的完整方法论（我承认没跑通的那部分） |
| [[reliability.resilience.retries]] | 重试、退避、以及重试如何放大故障 |
| [[reliability.resilience.containment]] | 熔断、隔板、降级——故障如何被围住 |
| [[monitoring.lag-e2e]] | 消费滞后与端到端延迟监控 |
| [[monitoring.metrics-and-slo]] | Kafka 侧的指标体系 |

相邻的几份：[[10-correctness-idempotency]]（1.5 那层监控的终极形态是对账）、[[03-snowflake-warehouse]]（Quality-Check 框架的实现细节）、[[06-cicd-progressive-delivery]]（发布出问题时的回滚路径）。

事故原文在 本机 `raw/slack`，工单在 本机 `raw/jira`，设计文档在 本机 `raw/confluence`。
