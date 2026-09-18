---
title: TS06 · CI/CD 与灰度发布
aliases:
  - TS06
  - CI/CD 灰度发布
tags:
  - interview/stack
  - stack/cicd
stories: [S5, S1]
---

# 06 · CI/CD 与渐进式发布（CI/CD / Progressive Delivery）

> 知识层（想更深时去哪）：[[CDN Content MOC|cdn-content]]：[[delivery.cicd]] · [[delivery.canary]] · [[delivery.shadow]] · [[delivery.rollback]] · [[delivery.flags]] · [[delivery.compatibility]]；[[System Design MOC|system-design]]：[[infra.delivery]] <!-- domain-links -->
> 适用于：JD 上出现"CI/CD"、"progressive delivery"、"feature flag"、"blue-green"、"canary release" 的岗；被问"讲讲你们怎么发布"、"上线出问题怎么办"、"这种改动你怎么灰度"。
> 不适用于：k8s 流量层金丝雀(按 pod 比例分流)、服务网格(Istio/Linkerd)灰度、A/B test 实验平台——这些我没有一手经验，见第 5 节。

---

## 0. 这个栈在 JD 里到底在问什么

JD 上写 "CI/CD" 或 "progressive delivery"，面试官心里通常在问三件事之一：**(a) 你们怎么把代码从提交到上线**（纯流程题，考流水线阶段划分）；**(b) 一个有风险的改动你怎么控制爆炸半径**（这是重点，考灰度/开关/回滚的具体机制，不是背模板）；**(c) 出问题之后你怎么应对**（考回滚 vs 前滚的判断力，以及"发布"和"生效"是不是同一件事）。这篇文章的第 2 节回答的主要是 (b)：我们的系统做灰度发布的方式跟教科书里典型的"k8s 按流量比例切一部分请求"完全不同——我们是在**数据层**做的,这个反差本身就是最好的深挖素材。

---

## 1. 来龙去脉

### 1.1 没有它的时候，人们怎么做，痛在哪

设想最原始的发布方式：写完代码，直接把新版本部署到所有生产机器上，覆盖旧版本。这在早期确实是默认做法——一台服务器，改完重启。问题在于**"部署"（deploy）和"生效"（release）被绑成了同一个动作**：代码一旦跑起来，全部用户立刻看到新行为。这带来两个致命问题：

第一，**没有退路**。如果新代码有 bug，唯一的补救是把旧代码重新部署一遍——这意味着从"发现问题"到"恢复正常"之间有一整个"回滚部署"的耗时窗口，期间所有用户都在经历故障。第二，**没有观察窗口**。你永远是先让 100% 的用户承受风险，再看数据判断对不对——如果这个改动会导致收费算错、数据丢失、订单状态错乱，这 100% 的冲击是没法收回的（compensating action 可能，但"没发生过"是回不去的）。

真实的痛点场景：一个电商网站要上线新的价格计算逻辑，如果直接全量部署，一旦逻辑有 bug，可能是几万笔订单价格算错，钱已经从用户账户划走或者商户已经按错误价格发货——这时候"回滚代码"解决不了"钱已经算错并且流动出去了"这个既成事实。

### 1.2 核心抽象

渐进式发布的核心抽象是把"**部署**"（把新代码放到生产环境）和"**发布**"（让新代码对用户/业务生效）拆成两个独立的动作，中间插入一个可控的、可观察的、可撤销的过渡区间。这个拆分衍生出一整套梯度手法，按"暴露给谁"和"暴露多少流量/数据"两个维度递进：

- **Feature flag（功能开关）**：部署时代码带着新逻辑一起上线，但用一个运行时可读的布尔/枚举值控制是否执行——部署这个动作本身完全不触发行为变化。这是最基础的一层，其余所有手法都建立在"有一个能被外部改变的开关"这个前提上。
- **Canary（金丝雀）**：打开开关，但只对一小部分**真实流量/真实对象**生效（1% 的请求、指定的几个用户、指定的一批商户），其余走旧路径。核心思想是"用可控的小样本承担风险，换来真实环境下的信号"。
- **Shadow / dark launch（影子/暗启动）**：新逻辑跟旧逻辑**同时**对同一份输入运行，但新逻辑的输出不对外产生任何真实副作用（不返回给用户、不落库生效），只用来跟旧逻辑的结果做比对。这是比 canary 更保守的一步——canary 让新逻辑真的影响一部分真实世界，shadow 完全不影响真实世界，只验证"如果生效了会不会算错"。
- **Blue-green（蓝绿部署）**：整套环境（不只是一个开关）复制成两份，流量在两份环境之间整体切换。切换是原子的、可瞬间切回的，代价是需要两倍的资源常驻。

这四种手法解决的都是同一个问题——"如何在生效之前，用真实但有限的方式验证正确性"——只是"有限"的维度不同：flag 限制的是"要不要生效"，canary 限制的是"对多少真实对象生效"，shadow 限制的是"生效但不产生真实副作用"，blue-green 限制的是"生效但可以整体撤回"。

### 1.3 关键权衡

**买到什么**：故障爆炸半径可控（1% 流量出问题不是 100%），观察窗口存在（有机会在扩大范围前发现问题），回滚代价降低（关一个开关比重新部署快得多）。

**代价是什么**：
- **系统复杂度上升**。每加一层灰度手法就多一条代码路径需要维护、测试、最终清理——一个功能全量上线之后如果不删掉判断分支和旧路径，代码库会堆积越来越多"永久存在的临时开关"，这是 flag-driven 架构的通病（见第 2 节 GRRCN 案例的类似问题）。
- **状态不一致的时间窗口被拉长**。灰度期间，系统里同时存在"走新逻辑的对象"和"走旧逻辑的对象"，任何跨对象的聚合、报表、对账逻辑都必须知道这种混合态的存在，否则会把灰度期间的差异误判为 bug。
- **它拒绝服务的场景**：**渐进式发布解决不了"新旧版本不兼容"的问题**。如果新逻辑改变了数据格式、表结构、协议字段的含义，灰度本身不会让这件事变安全——一旦一部分流量写入了新格式的数据，而另一部分代码（回滚后的旧版本，或者尚未升级的下游消费者）还在按旧格式读，就会读出错误结果或直接崩溃。这就是为什么"向后/向前兼容"是这整套手法的**前置条件**而不是可选项：你不能对一个破坏性的 schema 变更做金丝雀，因为金丝雀假设"新旧版本可以共存"，而破坏性变更恰恰打破了这个假设。

### 1.4 演化到今天

早期（单体、手动部署时代）没有这套区分，部署即发布。随着系统规模变大、单次故障影响面变大，行业逐步把"部署"和"发布"拆开：先是应用层的 feature flag（LaunchDarkly 这类产品的出现是这一步的标志），然后是基础设施层的流量灰度（k8s + service mesh 按比例分流请求），再到今天更细粒度的"渐进式交付"（progressive delivery）概念，把金丝雀分析自动化（根据错误率、延迟等指标自动决定继续放量还是自动回滚，如 Flagger/Argo Rollouts）。今天的默认选择是：**能不重启进程就不重启**（用开关而不是重新部署来控制生效），**能小范围先验证就不大范围**（canary 是默认心智模型），**破坏性变更必须先做兼容层**（双写、双读、影子验证）。

值得强调一点：教科书和大部分公司博客默认把"渐进式发布"讲成**流量层**的事情——k8s Ingress 按百分比分流、service mesh 按 header 路由。但灰度的核心抽象（部署与发布解耦、小范围先验证、可撤销）并不天然要求流量层实现；下一节要讲的系统，把同样的抽象整套搬到了**数据层**——一个从不面向 HTTP 流量、只处理 Snowflake SQL 批处理任务的系统里，一样能做出完整的 flag → canary → shadow → 回滚 这一套手法，只是载体是 SQL 里的 `IS_FEATURE_ACTIVE()` 判断和 Snowflake task 的开关，而不是 Kubernetes 的流量规则。

---

## 2. 在我们这套系统里它怎么用

### 2.1 架构位置

我在 Braintree Pricing & Settlement 团队维护的 `snowglobe` 是一个批处理式的记账与费用计算引擎：Java 17 + Gradle 管理 Flyway 迁移，但业务逻辑绝大部分是 Snowflake SQL——存储过程、UDTF、Stream、Task。它没有面向终端用户的 HTTP 接口，因此这里完全不存在"给 1% 的请求路由到新版本 pod"这种流量层灰度的落地场景。但它每天要处理真实的资金结算，任何一次数据源迁移、计算逻辑变更都可能直接影响商户能不能收到正确金额——发布风险不比一个面向用户的 Web 服务小，只是**载体是 SQL 任务而不是 HTTP 服务**。灰度机制因此完整地实现在数据层：`IS_FEATURE_ACTIVE(flag_name)` / `IS_MERCHANT_ACCOUNT_FEATURE_ACTIVE(flag_name, region, merchant_id, timestamp)` 这两个 SQL 函数，是这套系统里 feature flag 的落地形态；CI 用 `ci.braintree.tools` 上的 Jenkins（`snowglobe/README.md` 顶部的 build badge 直接指向这个 Jenkins job）跑测试和部署 Flyway 迁移。

### 2.2 关键 feature 与设计决策

**(1) SQL 里的全局 feature flag：`US_CREDIT_INTERCHANGE_FROM_SETTLE_ENABLED`**

**机制**：一个 Snowflake task（`FETCH_FISERV_CREDIT_INTERCHANGE_FROM_SETTLE_STAGING`，代码 `app/src/main/resources/db/squashed/V20251105120000__create-fetch-fiserv-credit-interchange-from-settle-task.sql`）在执行体最外层包一个 `IF (IS_FEATURE_ACTIVE('US_CREDIT_INTERCHANGE_FROM_SETTLE_ENABLED')) THEN ... END IF`，开关的默认值在迁移文件里显式插入为 `FALSE`（`INSERT INTO SYSTEM_TOGGLES (FEATURE_NAME, ACTIVE) VALUES ('US_CREDIT_INTERCHANGE_FROM_SETTLE_ENABLED', FALSE)`）。这是 PR #1615（"Fetch interchange fee from settle view instead of trans view"，+634/-39，2025-11-20 合并）把美国信用卡 interchange 费用的数据源从到达晚的 Fiserv `TRANS` 视图切到到达更早的 `SETTLE` 视图这一改动的整体开关。

**替代方案**：旧代码里其实已经有一套"哪个视图有数据就用哪个"的**动态 fallback 逻辑**（多个 CTE：PARAMS、STATUS、DECISION，运行时判断用哪个数据源）。PR body 原话点出这个旧方案的问题："High System Complexity: Dynamic fallback logic with sticky behavior, multiple CTEs... increase maintenance burden"。

**为什么选了静态开关而不是动态 fallback**：迁移选择的方向是"按费用类型做静态职责划分"——interchange 固定走 Settle，其余（scheme/chargeback/auth/non-tran）固定走 Trans/Auth/Non-Tran，一个 boolean flag 整体控制切换与否,而不是运行时判断"哪个源有数据就用哪个"。这是用**部署时确定性**换**运行时智能**——旧方案更"聪明"（自动挑数据源），新方案更"笨"但可预测、可灰度、可回滚。

**代价**：老 task（`FETCH_FISERV_CREDIT_PASS_THROUGH_FEES_STAGING`）被同一个开关反向改造，加了一个显式排除条件（`IS_FEATURE_ACTIVE(...) = FALSE OR ... != 'interchange'`），开关关闭时老 task 抓取全部费用类型（含 interchange），开关打开后老 task 显式排除 interchange 记录。这是"双写切换"里最容易出错的一步——必须保证同一时刻只有一条 task 在产出 interchange 记录，否则会重复计费。团队把这个互斥关系维护对了，但代价是新老两个 task 现在永久耦合在同一个开关上，改任何一边都要想清楚对另一边的影响。

**(2) 商户级 canary：`IS_MERCHANT_ACCOUNT_FEATURE_ACTIVE`**

**机制**：跟上面的全局开关不同，`IS_MERCHANT_ACCOUNT_FEATURE_ACTIVE(feature_name, region, merchant_account_id, timestamp)` 是按**单个商户账户**粒度判断某功能是否生效的 UDF，读取四张表（`MERCHANT_ACCOUNT_FEATURES_GLOBAL`、`MERCHANT_ACCOUNT_FEATURES_REGIONAL`、`MERCHANT_FEATURES`、`MERCHANT_ACCOUNT_FEATURES`）按"全局 → 地区 → 按商户 → 按商户账户"优先级判断，低优先级的"关闭"不能覆盖高优先级的"开启"。这本质上是这套系统里**真正意义上的金丝雀队列**——不是按流量百分比随机采样，而是按业务对象（商户）显式圈定一个可控子集。

**为什么是商户级而不是全局**：这套开关体系是从 `funding` 服务同步过来的"影子实现"——`funding` 侧原本就有 `MerchantAccountFeature`（临时性、支持按商户账号灰度）和 `MerchantFeature`（永久性能力开关）两层区分，`snowglobe` 侧用同一套 UDF 在 SQL 层复刻这个优先级判断逻辑，两边必须保持逻辑一致。选择商户粒度而不是全局粒度，是因为很多变更（比如新的日记账流程 `JOURNAL_TRANSACTIONS`）天然是"某些商户先接入新流程，其余商户保持旧流程"的迁移场景，而不是"一刀切全体切换"。

**代价**：两套开关体系（`funding` 的 Ruby 实现 + `snowglobe` 的 SQL UDF 影子实现）必须逻辑保持一致，一旦漂移，同一个商户账号在两个系统里会出现"该开的没开、不该开的开了"的不一致——这是维护两份"同一份真相的复刻实现"的通病。

**(3) SQL 里叠加的多层闸门：一条 MERGE 里的三种独立判断**

上面 PR #1615 的核心 procedure `COPY_FISERV_CREDIT_INTERCHANGE_FROM_SETTLE_TO_PASS_THROUGH_FEES_STAGING` 里，`WHERE` 子句同时叠了三层过滤：`IS_MERCHANT_ACCOUNT_FEATURE_ACTIVE('JOURNAL_TRANSACTIONS', ...)`（商户级功能开关，判断这个商户是否已接入新日记账体系——注意这是一个跟迁移无关的独立业务开关）、上面提到的全局迁移开关（挂在调用这条 procedure 的 task 上）、以及 `SETTLE.PRDT_CD_ORG != '00006'`（产品代码层面直接排除 Amex，因为 Amex 走另一条完全独立的 GRRCN 流水线）。

**机制**：迁移能不能整体生效由 task 级开关控制，单个商户是否已接入新日记账体系由商户级开关控制，业务上不该出现在这条支路的记录（Amex）在源头就被静态剔除——三个正交的维度叠在同一条 SQL 里。

**为什么这样设计**：这是"灰度上线"场景里一个容易被忽略但很典型的模式——不同的开关回答不同的问题（"这次迁移生效了吗"vs"这个商户走新流程吗"vs"这条记录本来就不该走这里"），把它们混成一个开关会导致"关掉迁移开关"这个动作意外影响到跟迁移完全无关的商户级功能。

**代价**：多开关叠加容易在环境间产生组合不一致（比如 sandbox 全开、prod 只开一半），这是 flag-driven 架构的通病；具体到这套系统，两个独立开关（`AGGREGATED_AMEX_SEPARATE_FLOW` 和 `EU_AGGREGATED_AMEX`，见另一条 Amex GRRCN 流水线）就出现过这种排列组合复杂度——若前者打开而后者未打开，走 US OptBlue 逻辑；两者都打开才走 EU 分支。

**(4) 影子验证：Trans View → Settle View 切换前的两阶段核验**

这是这套系统里**最接近"shadow / dark launch"教科书定义**的实践,但它验证的不是"新逻辑跑起来是否报错"，而是"新数据源的数据本身是否可信"：

- **发现阶段**（Confluence pageId `2698298357`）：用 `FULL OUTER JOIN` + `EQUAL_NULL` 逐字段比对 Settle 与 Trans 两侧归一化后的记录，字段包括 currency/brand/network/wallet/plan/amount/rate/fixed/mid/arn。结论：两侧字段级一致率 >99.9%，不匹配率约 **0.07%**（且这些不匹配是"当天只有一侧有记录"，不是真正的数值冲突）。
- **切换前验证**（Confluence pageId `2747965111`）：用**即将上线的生产查询本身**（同样的 `CLX_TRIGGER_STATUS_V1` 握手条件、同样的 Amex 排除条件，只是把 `SELECT ...` 换成 `SELECT count(*)`）对当天全量做行数比对：TRANS 视图 13,737,670 行，SETTLE 视图 13,768,430 行，差异率 **0.224%**，结论是"覆盖率接近 100%，差异在可接受范围内"。

这两个数字**衡量的是两件不同的事**，不能混用：0.07% 是"两边都有记录时字段是否一致"，0.224% 是"两边记录数量本身的差异（含只有一边有记录的情况）"。

**为什么用生产查询本身做验证，而不是抽样估算**：验证逻辑和生产逻辑同源，减少了"验证时用一套口径，上线后用另一套口径"的错配风险——这是"影子跑一遍生产逻辑，只是不让结果生效"这一手法在批处理系统里的具体落地：没有一个专门的"影子环境"，而是把同一段生产 SQL 换个 SELECT 目标，跑在真实数据上但不写入生产表。

**灰度计划本身**（Confluence 原文）：1) 开关关闭部署代码（验证部署本身无误）；2) sandbox/dev 环境打开开关；3) 观察差异率与数据质量；4) 生产环境逐步放量。这是标准的"先关后开、中间插观察窗口"模式，PR #1615 自带的 "Database migration checklist" 也显式勾选了"新增列必须可空"等一系列 Snowflake 迁移安全规则，说明这类变更有制度化的 checklist 把关，不完全依赖个人经验判断。**诚实说明**：文档只给出了 rollout 计划的**意图**，没有找到"sandbox 打开后观察了多久、prod 是分批还是一次性打开"这类**执行记录**——PR #1615 自己 "How will you verify the success of this change in QA and production?" 一栏填的是 "N/A"。计划层面有据可查，执行细节这一步如实标注为未验证，而不是编造一个听起来合理的时间线。

**(5) 兼容性作为前提：老任务的"互补排除"条件**

上面提到，开关打开后老 task（`FETCH_FISERV_CREDIT_PASS_THROUGH_FEES_STAGING`）被反向改造为显式排除 interchange 记录。这行看似不起眼的排除条件，实际上是"能不能安全灰度"的**前提**——如果没有这个互补排除，灰度期间（新老 task 短暂共存的窗口内）会出现双写：新 task 按新数据源产出一条 interchange 记录，老 task 按旧路径也产出一条，同一笔费用被算了两遍。这正是第 1.3 节说的"渐进式发布买不来兼容性,你必须自己把兼容性做出来"的具体例子：灰度机制（开关）本身不会自动帮你处理新老逻辑共存期间的数据冲突，团队必须在 SQL 里显式写出"新逻辑生效时老逻辑要让路"这条互斥规则。

**(6) CI 与开发环境隔离：Jenkins + Flyway + snowglobe-tools 的 schema pool**

CI 跑在 `ci.braintree.tools` 上的 Jenkins（`snowglobe/README.md` 顶部的 build badge 直接指向这个 job），负责跑测试、执行 Flyway migration。Flyway 本身是"部署"这一步的具体执行者——迁移文件按版本号（`V...`）和可重复（`R__...`）两类管理，`flyway_schema_history` 表记录哪些迁移已经跑过，这保证了"同一份迁移永远只跑一次、可重复迁移检测到修改会重跑"。

这套体系有一个我自建的辅助工具值得一提：`snowglobe-tools`（`czhang17_paypal/snowglobe-tools`，个人仓库，无 ticket 驱动）里的 `schema-pool` 项目，解决的是"多个 Claude Code agent session 同时在不同分支上跑 Snowglobe 集成测试,会因为共用同一个 Snowflake schema/database 而在 DDL、Flyway migration 上互相打架"的问题——这不是生产发布的灰度机制，而是**开发环境侧**为了支持多分支并行验证而做的隔离，跟 CI/CD 的关系是"让每次 PR 的测试环境互不干扰"。详见 2.3。

### 2.3 我做的部分 `[me]`

以上机制里，直接由我设计和实现的部分：

- **PR #1615**（"Fetch interchange fee from settle view instead of trans view"，+634/-39，11 文件，2025-11-20 合并）——2.2 节 (1)(3)(4)(5) 描述的整套开关设计、SQL 里的多层闸门、以及两阶段核验（discovery + 切换前验证），均由我完成。两份 Confluence 设计文档（pageId `2698298357` discovery、`2747965111` 切换前验证）也是我写的，含 `FULL OUTER JOIN` 字段级比对的 SQL 与量级对比的原始数据。
- **`snowglobe-tools`（`schema-pool`）**——个人建的开发环境隔离工具，全部 23 个 commit 直接 push 到 `main`（无 PR 流程，单人开发）。V2 重写（`SCHEMA_POOL_V2`，commit `42364e1`）把 pool 的克隆源从"直接 clone PUBLIC schema"（不稳定，取决于谁最后跑了什么迁移）改成"先维护一个从生产实际部署 SHA（通过 GitHub Deployments API 查询，而不是 release tag——因为 tag 可能打了但没真正部署）同步的 MAIN schema，再从 MAIN 批量 clone 出 POOL_N"，这个决策记在 ADR-0002（`0002-default-sync-target-is-prod-deployment-sha.md`）。另两篇 ADR：ADR-0001 规定 sync 操作必须在本地跑（不能放 CI/CPAIR 远程环境，因为依赖本地已有的 Snowflake 会话和 git checkout 状态）；ADR-0003 记录 sync 流程刻意跳过 `share` 模块的 Flyway migration 且明确标注"不要修复这个"（已知的、故意保留的限制）。Flyway 边界情况的具体处理：跨库 clone 顺序问题（commit `0d6e94c`：必须先 clone `REPL_DB` 再 clone `APP_DB`，否则 `APP_DB` 里依赖 `REPL_DB` 表的 stream 会失效，后续 `8365985` 把这个已知模式做成 swap 后的自动修复逻辑）、`db/test/` 目录下重复的 repeatable migration 排除（`f633677`）、仅生产环境存在的上游表用 stub 表打通本地依赖（`c4f91bf`，这个方案本身不稳定，紧接着一整天 10 个 commit 都在修它踩的坑：Kotlin DSL 语法错误、`USE SCHEMA` 上下文丢失、多语句 SQL 需要用 `snow sql --filename` 而非内联字符串）。

**没做过的部分**：PR #1615 描述的四步走灰度计划，"sandbox 打开后观察了多久、prod 具体怎么分批"这类执行记录我没有找到可引用的证据（连 PR 本身的 QA/生产验证方式一栏都填的是 N/A），如实说没做这步的完整记录，而不是编。

---

## 3. stripe kit 考到的点

Stripe OA/机考里几乎不会直接问"你会不会做灰度发布"——这类知识不是以"写一个 CI/CD 流水线"的题目形式出现，而是**藏在题目的约束条件里**。最直接相关的是幂等/去重这条线：[[s11-idempotency-dedup|S11 幂等 / 去重]] 考的是"重复的操作要被忽略/覆盖/报错"这三种语义的区分——这正是渐进式发布里"新老路径短暂共存、可能产生重复写入"这一风险的题目化版本（本文 2.2 节 (5) 的"互补排除"条条本质上就是在解决这个问题的生产版本）。另一个相关点是 [[s17-ledger-balance-tracking|S17 台账式余额跟踪]]——如果一道题要求"某个开关/状态切换后，历史记录和新记录的口径要能共存被正确读出"，本质上是在考"新旧版本共存期间数据一致性"这个 progressive delivery 的前置条件（1.3 节讲的"没有兼容性，灰度买不来安全"）。总体而言，这个栈的知识在机考里更多体现为"你的状态机/幂等设计能不能优雅处理版本切换过程中的中间态"，而不会直接问"什么是 canary"。

---

## 4. 常见追问与答法

| 追问 | 一句话答 | 展开的抓手 |
|---|---|---|
| 什么是 blue-green、canary、feature flag 的区别？ | flag 控制"要不要生效"，canary 控制"对多少真实对象生效"，blue-green 是整套环境切换。 | 1.2 节三者定义 + 各自的暴露维度 |
| 部署和发布为什么要分开？ | 分开之后，代码上线这个动作本身不再触发风险，风险敞口从"发现问题的整个部署耗时"缩短到"翻转一个开关的耗时"。 | 1.1 节的"没有它会怎样"场景 |
| 你们做灰度是流量层还是应用层？ | 我们的系统是批处理引擎，没有 HTTP 流量层，灰度整套搬到数据层：SQL 里的 feature flag + 商户级 canary + 影子核验。 | 2.1–2.2 节 |
| 商户级金丝雀跟流量按百分比灰度有什么不同？ | 流量灰度是随机采样一部分请求，商户级灰度是显式圈定一个真实业务对象子集——可控性更强（知道具体是谁受影响），但需要业务侧本来就有"按对象分组"这个粒度存在。 | 2.2 节 (2) |
| **[第三层]** 如果你的开关组合在 sandbox 和 prod 之间不一致会怎样？ | 会产生"同一份代码在不同环境走不同分支"的排列组合复杂度——我们的系统里 `AGGREGATED_AMEX_SEPARATE_FLOW` 和 `EU_AGGREGATED_AMEX` 两个独立开关就出现过这个问题，必须靠人工核对环境间开关状态，框架本身不保证一致性。规模再大十倍，这种人工核对方式会失效，需要一个"开关状态对比工具"把环境间差异自动列出来——我们目前没有这个工具，是一个已知但未解决的缺口。 | 2.2 节 (3) |
| **[第三层]** 灰度期间如果新旧逻辑都在写同一份数据，你怎么验证没有重复计费？ | 光靠开关本身验证不了，必须在 SQL 里显式写互斥条件，并且要有一个独立的核验步骤（不是靠信任开关切换的原子性）——我们的做法是把生产查询本身改成 count(*) 在真实数据上跑影子核验，而不是靠人工推理"应该不会重复"。这也是为什么我认为"验证用的逻辑要和生产逻辑同源"比"额外写一套单测"更可信,因为单测数据是构造的,不会暴露生产数据里真实存在的边界情况。 | 2.2 节 (4)(5) |

---

## 5. 我的边界

**边界在哪**：我没有 Kubernetes 流量层灰度（按 pod 比例切流量、Istio/Linkerd 按 header 路由）的一手实现经验；也没有做过面向终端用户的 A/B test 实验平台或自动化金丝雀分析（根据错误率自动决定放量/回滚，如 Flagger/Argo Rollouts）。

**我怎么说**：我会直接说清楚——"我做灰度发布的经验全部在数据层，不是流量层；如果你问的是 k8s 层面的滚动更新/金丝雀部署机制本身，我知道概念和常见实现方式，但没有一手运维经验"。不硬撑成"我也做过 k8s 灰度"，因为一旦被追问具体命令、具体 CRD 字段就会露馅。

**能把话接到哪去**：能接回的是——虽然载体不同（SQL 任务 vs HTTP 流量），我在数据层做的这套（feature flag → 商户级 canary → 影子验证 → 显式互斥回滚）覆盖了渐进式发布的**全部核心抽象**，而且是在一个"发布出错等于资金结算出错"这样风险不亚于用户面服务的系统里完整实践出来的。如果面试官继续追问"那你怎么判断这套经验能不能迁移到流量层场景"，我的答案是：**核心决策（要不要发布、发布给谁、多快能收回）是相通的，变的只是"发布对象"的粒度单位（请求 vs 商户账户）和"回滚"的执行方式（改路由规则 vs 翻转 SQL 开关）**——这是我在准备这篇文章时想清楚的一层抽象,可以在面试里主动讲出来,而不是被问到才想到。

---

## 6. 往深里看

- [[delivery.cicd]]——CI/CD 流水线阶段划分本身，什么时候该去读：想知道一条标准流水线（build → test → deploy → release）该怎么拆分阶段职责时。
- [[delivery.canary]]——金丝雀发布的流量层实现细节，想知道 k8s/service mesh 里具体怎么按比例分流时去读，可以对照本文 2.2 节的商户级 canary 做类比。
- [[delivery.shadow]]——影子/暗启动的更多变体（比如双写但只信一份），想深挖"影子验证"这个手法的其他实现方式时去读。
- [[delivery.rollback]]——回滚 vs 前滚的判断标准，被问"什么时候该回滚、什么时候该继续推进修复"时去读。
- [[delivery.flags]]——feature flag 的生命周期管理（何时清理、如何避免永久堆积），对应本文 1.3 节提到的"复杂度上升"问题。
- [[delivery.compatibility]]——向后/向前兼容的具体判定方法，1.3 节"灰度买不来兼容性"这句话的详细展开。
- [[infra.delivery]]——system-design domain 里对交付/发布这条主线的通用框架，想把这篇文章的具体案例接回系统设计面通用答法时去读。

本栈相关的 readings 见 `vault/domains/cdn-content/readings/delivery-google-canarying.md`、`delivery-kubernetes-deployments.md`；cards 见 `vault/domains/cdn-content/cards/delivery/`（含 `delivery-canary-ramp-guardrail.md`、`delivery-flags-lifecycle.md`、`delivery-shadow-divergence.md` 等）。
