---
title: TS04 · Terraform / IaC
aliases:
  - TS04
  - Terraform
tags:
  - interview/stack
  - stack/terraform
stories: [S8]
---

# 04 · Terraform / 基础设施即代码（Infrastructure as Code）

> 知识层（想更深时去哪）：[[CDN Content MOC|cdn-content]]：[[delivery.terraform-kubernetes]] · [[delivery.cicd]] · [[delivery.aws]] <!-- domain-links -->
> 适用于：JD 上出现 Terraform / IaC / CloudFormation / Pulumi；被问"你们的基础设施怎么管的"、"权限怎么授的"。
> 不适用于：多云架构、大规模 Terraform 治理（workspace 拆分策略、Terragrunt、Atlantis）——见第 5 节。

---

## 0. 这个栈在 JD 里到底在问什么

**一、你改基础设施的时候，别人看得见吗。** 这是 IaC 的全部意义。手工点控制台的人和提 PR 改 `.tf` 的人，区别不在效率，在于后者的每一次变更都有 diff、有 review、有 git blame。

**二、你踩过 state 的坑没有。** Terraform 的威力和它的危险来自同一个东西——那个记录"我认为世界是什么样"的状态文件。没被 state 坑过的人，多半只跑过 demo。

**三、你知不知道 `apply` 不等于安全。** IaC 让变更可复现、可审查，但**不会让它变得不危险**。一个 `terraform apply` 照样能删掉生产数据库。知道这个区别的人，才会去设计 plan review 和权限边界。

---

## 1. 来龙去脉

### 1.1 IaC 之前：雪花服务器和它的三个症状

在基础设施靠人手工配置的年代，典型的故障排查是这样的：生产环境有个服务跑得好好的，你照着文档在测试环境搭一套，跑不起来。查了三天，发现三年前有人在生产机器上手动装过一个包、改过一行 `sysctl`，没写进任何文档，那个人已经离职了。

这台机器就是**雪花服务器（snowflake server）**——独一无二，无法复制，没人知道它为什么能工作。它有三个症状：

- **漂移（drift）。** 声称的配置和实际的配置不一样，而且差距随时间单调增长。每一次"临时改一下，回头补文档"都在加深它。
- **不可复现。** 重建一台等价的机器是考古工作，不是工程工作。灾难恢复演练做不了，因为没人敢保证重建出来的是同一个东西。
- **没有审计线索。** "谁在什么时候改了什么、为什么" —— 这三个问题没有答案。出了事只能靠人回忆。

### 1.2 核心抽象：把期望状态写成代码，让工具去收敛

IaC 的转念很简单：**不要描述步骤，描述结果。**

对比两种写法：

```bash
# 命令式：描述步骤
aws s3 mb s3://my-bucket
aws s3api put-bucket-versioning --bucket my-bucket --versioning-configuration Status=Enabled
```

```hcl
# 声明式：描述结果
resource "aws_s3_bucket" "main" {
  bucket = "my-bucket"
}
resource "aws_s3_bucket_versioning" "main" {
  bucket = aws_s3_bucket.main.id
  versioning_configuration { status = "Enabled" }
}
```

命令式脚本**只能跑一次**：第二次跑，`mb` 会因为 bucket 已存在而失败。要让它可重复，你得自己写一堆"如果不存在才创建"的判断——而这正是声明式工具替你做的事。

声明式的完整回路是三步：**读取期望状态（你的 `.tf` 文件）→ 读取实际状态（调云 API）→ 算出差异并收敛**。这个"算差异"的能力带来了两个衍生品：

- **`terraform plan`** —— 在改动发生之前，看到它会做什么。这是 IaC 相对于脚本最大的单项优势：**一个可以被 review 的、关于未来的 diff**。
- **幂等** —— 已经是期望状态时，apply 什么也不做。这让"定期 apply 一次"成为一种纠偏机制，而不是一次冒险。

### 1.3 State：让它工作的东西，也是咬你的东西

Terraform 需要知道"我管理的资源现在是什么样"。它把这个记在**状态文件**里——一份资源清单，把你代码里的 `aws_s3_bucket.main` 映射到云上那个真实 bucket 的 ID。

为什么不能每次都去云上现查？因为查不全：云 API 能告诉你"有哪些 bucket"，但不能告诉你"哪些是这份配置管的"。state 就是那条归属线。

它带来四类真实的麻烦：

- **并发。** 两个人同时 apply，state 会写坏。所以要远程 state 加锁（S3 + DynamoDB 是经典组合）。
- **漂移仍然存在，只是换了形式。** 有人手工改了云上的东西，state 不知道。下次 plan 会显示一个你没预期的 diff——这是好事，但前提是有人在看。
- **state 里有敏感信息。** 数据库密码、私钥会明文进 state。所以 state 要加密、要控制访问，而且不能进 git。
- **重构代码会误伤资源。** 把资源改个名或挪进 module，Terraform 会认为"旧的没了、新的要建"——于是删掉重建。`terraform state mv` 和 `moved` block 就是为此存在的。**这是新手最容易造成生产事故的地方：一次看起来无害的重命名。**

### 1.4 模块与组合

`module` 是 Terraform 的复用单元：一组资源加上输入变量，可以实例化多次。

抽模块的判据和抽函数一样——**同一个模式出现了三次**。过早抽象的模块会有一大堆为了兼容所有调用方而存在的 `variable`，比复制三份还难读。这是 IaC 里同样成立的普遍规律。

### 1.5 关键权衡：IaC 买到了什么，没买到什么

**买到了**：可复现、可审查、有审计线索、能纠偏。

**没买到的，必须说清楚**：

- **安全性。** `terraform apply` 照样能删生产库。plan 里那行 `-/+ destroy and then create` 需要人看见并且看懂。**IaC 让危险操作变得可见，不是变得不危险。**
- **对不支持的东西的覆盖。** provider 没实现的资源类型，只能手工或者 `null_resource` 兜底，而那些兜底就是新的雪花。
- **零学习成本。** HCL 的循环、条件、动态块写起来相当别扭，团队里总有人写出没人敢改的模块。

**演化到今天**：默认选择从 CloudFormation（云厂商自带、只管自家）转向 Terraform（跨 provider、生态大）；再往后有 Pulumi 和 CDK 这类"用真正的编程语言写"的方案——它们换来了表达力，代价是失去了 HCL 的受限性所保证的可预测性。大多数团队的答案仍然是 Terraform。

---

## 2. 在我们这套系统里它怎么用

这里的用法有个不寻常的地方，值得作为整节的主线：**Terraform 管的不是服务器，是 Snowflake 这个数据平台本身**，而且它描述的东西里有一大块其实是数据管道。

### 2.1 用 Terraform 管一个数仓

`snowglobe-terraform` 仓库用 `snowflake` provider 管理的资源类型包括：

```
snowflake_database            snowflake_schema           snowflake_table
snowflake_stream_on_table     snowflake_task             snowflake_procedure_sql
snowflake_function_sql (UDTF) snowflake_account_role
snowflake_grant_ownership     snowflake_grant_privileges_to_account_role
```

注意这个清单的后半段：**存储过程、UDTF、task、stream 都是 Terraform 资源**。也就是说业务逻辑的一部分（至少是它的容器和调度）被声明在 `.tf` 文件里，而不只是基础设施。

这是个真实的取舍，面试里值得展开：
- **好处**：数据管道的全套组件（表、流、任务、过程、权限）在一个地方声明、一起 review、一起 apply，不会出现"表建了但 task 忘了建"这种半拉子状态。
- **代价**：SQL 逻辑被包在 HCL 字符串里，失去了 SQL 工具链（格式化、lint、语法高亮）。而且 Snowflake 里同一件事有两条路——Flyway 迁移和 Terraform 资源——**边界在哪需要团队约定，约定不清就会出现两边都管或者都不管的资源**。

### 2.2 模块划分与那个反复出现的 CDC 模式

模块按业务域拆：`modules/cdc/`（通用 CDC 基础设施，单文件 `main.tf` 近 4000 行）、`modules/pricing/fee_anomalies/`、`modules/scheme_fees/`、`modules/merchant_performance/`、`modules/reporting/`、`modules/machine_learning/`、`modules/kafka-connect-role/`。

`modules/cdc/` 里反复出现的核心模式是：

```
Kafka CDC connector 把上游表的变更事件写进 Snowflake 原始表
  → snowflake_stream_on_table 检测新增行
  → snowflake_task 在 system$stream_has_data(...) 为真时触发
  → snowflake_procedure_sql 把数据 merge/upsert 进类型化目标表
  → 配套一个 snowflake_function_sql (UDTF) 解析原始 JSON/variant payload
```

**五个资源组成一条管道，整条管道是声明出来的。** 接一张新的上游表，等于实例化一次这个模块。这是 module 抽象用对了的例子——同一个模式重复了很多次，抽出来之后新增上游从"写五段 SQL 加一个调度"变成"填几个变量"。

这条管道在业务上的意义见 [[07-data-pipelines-cdc]]；这里关注的是它被声明的方式。

**一个值得注意的脆弱点**：`modules/cdc/main.tf` 里有指向 funding 仓库**具体 commit SHA** 的注释——那是这两个仓库之间最实锤的物理连接点。跨仓库的契约没有类型系统能保证，只能靠这种手写锚点，而它一定会过期。这是 1.5 里"IaC 没买到的东西"的一个具体实例。

### 2.3 我做的部分 `[me]`

我在 `snowglobe-terraform` 有 **5 个 PR**，方向集中在 grant / ownership。最值得讲的是 **PR #1326**。

**现象**：一次 release 卡住，`GRANT OWNERSHIP` on `FEE_ANOMALIES_DB` 被 Snowflake 拒绝。

**根因**：`FEE_ANOMALIES_REVIEWER` 这个角色已经持有该对象上的依赖 USAGE grant。Snowflake 在转移 ownership 时必须知道怎么处理这些既存的从属权限——是一起转走还是撤销——而 `snowflake_grant_ownership` 资源的 `outbound_privileges` 参数就是回答这个问题的。这个资源没写它，Snowflake 拒绝在歧义下执行。

**处理**：约 7 分钟定位，出 PR #1326，release 成功部署。（Slack `#treasury-services-releases`，2026-08-13，见 本机 `raw/slack`）

**关于这个故事的一处订正，以及它带来的更好素材。** 我原来的说法是"这是全 repo 唯一一个缺 `outbound_privileges` 的 `snowflake_grant_ownership` 资源"——**这个说法不成立**：79 个 `snowflake_grant_ownership` 资源里有 **42 个**缺这个参数。不过多数是 `future_*` 变体，风险等级低（未来对象上的 grant 通常还没有依赖关系纠缠）。

更有价值的是核查时发现的东西：`modules/scheme_fees/main.tf` 里的 `scheme_fees_dcm_ownership` 和 `scheme_fees_dcm_public_ownership` 两个资源，**属于同一类高风险场景且至今未修**。

面试里我会这样讲这件事：修一个 7 分钟的 bug 不算什么，**修完之后回头问"同样的问题还在哪"才算**。而且这个反查把我自己原来的说法证伪了——真实的数字比我记忆里的难看，但配上"42 个里多数是低风险的 future 变体，剩下两个是真风险且还没修"这个分析，反而是更强的技术叙事。

原始证据：[[S8]]。

---

## 3. stripe kit 考到的点

Terraform 本身不在 OA 考纲里。真正相关的是**声明式思维**和**幂等**，那两个是跨栈的：

- [[s11-idempotency-dedup|S11 幂等 / 去重]] —— `terraform apply` 的幂等和 MERGE 的幂等是同一个概念：重复执行结果不变
- [[s05-threshold-semantics|S05 阈值语义]] —— 关系不大，但 `outbound_privileges` 这个坑的形状和它很像：**一个参数不写不是"用默认值"，而是"让系统在歧义下拒绝"**，和"没写等号方向"翻掉隐藏测试是同一类失误

系统设计轮倒是常问基础设施怎么管，那时候第 2 节的内容直接可用。

---

## 4. 常见追问与答法

| 追问 | 一句话答 | 展开的抓手 |
|---|---|---|
| 为什么用 Terraform 不手工配 | 可复现 + 可 review + 有审计线索；手工配出来的是雪花服务器 | 1.1 的三个症状 |
| state 文件放哪 | 远程后端加锁，加密，绝不进 git | 1.3 的四类麻烦 |
| 有人手工改了云上资源怎么办 | 下次 plan 会显示非预期 diff——前提是有人在看 plan | 引出"定期 apply 作为纠偏机制" |
| 用 Terraform 管数据库对象合适吗 | 好处是管道组件不会半拉子，代价是 SQL 被包进 HCL、和 Flyway 的边界要约定清楚 | 2.1 的取舍 |
| **（三层）重命名一个资源会发生什么** | **默认会删了重建。这是最容易造成生产事故的无害操作** | `terraform state mv` / `moved` block；引申到"为什么 plan 必须逐行看" |
| **（三层）plan 看着没问题，apply 到一半失败了** | **Terraform 没有事务。部分资源已建、state 部分更新，需要重跑收敛** | 承认这是 IaC 的固有限制，接到"所以危险变更要拆小、要能重入" |
| **（三层）你修了 #1326，同类问题还有多少** | **42/79 缺这个参数，多数是低风险 future 变体；但 `modules/scheme_fees` 里两个是真风险，还没修** | 2.3。主动给出这个数字比等着被问出来强得多 |

---

## 5. 我的边界

**我不是这个仓库的主力，只有 5 个 PR，方向集中在 grant/ownership。**
→ 我会说："`snowglobe-terraform` 是团队共同维护的，我的贡献集中在权限和 ownership 这一块，`modules/cdc/` 那 4000 行不是我写的——我是它的下游消费者，读过但没建过。"
→ 接回去："不过权限这块我摸得比较透，#1326 那个 case 加上后来的反查，让我对 Snowflake 的 grant 依赖模型有了相当具体的理解。"

**大规模 Terraform 治理我没做过。** workspace 怎么拆、多环境怎么隔离、Terragrunt / Atlantis 这类工具链、state 拆分策略。
→ 我会说："我们的规模还没到需要这些的程度，单 repo 单 state 加 CI 跑 plan 就够用。我知道这些问题在更大规模上会出现，但没有实操。"

**多云和 AWS 本身的深度不够。** 我们的 Terraform 主要管 Snowflake，AWS 那侧（S3 stage 之类）是团队其他人配的。
→ 我会说："我用 Terraform 的场景比较特殊——管的是数据平台而不是计算资源。VPC、IAM、EKS 那套我没有生产经验。"

---

## 6. 往深里看

| 节点 | 什么时候去读它 |
|---|---|
| [[delivery.terraform-kubernetes]] | Terraform 与 K8s 的组合、state 管理、plan 审查的完整实践 |
| [[delivery.cicd]] | plan/apply 怎么接进流水线，谁有权 apply |
| [[delivery.aws]] | AWS 侧资源的组织方式（我的弱项，补课方向） |

相邻的几份：[[06-cicd-progressive-delivery]]（apply 作为发布动作的一环）、[[05-kubernetes]]（另一个声明式收敛系统，思想同源）、[[07-data-pipelines-cdc]]（2.2 那条 CDC 管道的业务含义）。

卡片在 `vault/domains/cdn-content/cards/delivery/`（含 `delivery-terraform-plan-state.md`），readings 在 `vault/domains/cdn-content/readings/`。
