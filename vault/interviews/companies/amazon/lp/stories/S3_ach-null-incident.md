# S3 · ACH 费用 NULL 传播事故（最难的 bug · fail loudly）

**A health check I built paged us because fees were silently missing — I found the cause in minutes, then removed the whole class of bug.**

## 适用 LP

- 主：**Dive Deep**、**Ownership**、**Insist on the Highest Standards**、**Have Backbone**
- 副：Customer Obsession、Bias for Action、Earn Trust、Deliver Results

## 数字

- 受影响 **~196 商户**，**~$11.3M/天** GMV：说 "roughly two hundred merchants, on the order of ten million dollars a day"
- 缺失 **~99,700** 笔 settled 费 + **~5,500** 笔 discount 费；累计 ~1.79M pending 行
- 切片：**100%** us_bank_account，**100%** STANDARD_ACH
- 事故发生在 standard-ACH **灰度**阶段（M2）；告警每日 **13:30 CT**
- 根因定位只说 "a few minutes"
- e2e 没抓到的 **4 个原因**

## S / T / A / R / L

### S
- 我建的每日**健康检查** "every settled transaction has its Braintree fee" 报警 page 了 on-call

### T
- 我不是 assignee；把 page **转给自己**，负责**根因、postmortem 和加固**

### A
- **切片**：缺失的 100% 是新 **standard-ACH** 路径的银行账户交易，~**200 商户**、~**$10M/天**
- **追一笔交易**：sub-kind 是 **NULL**，`'BT_' || NULL` 还是 **NULL**，无类别、无费用、**无报错**
- **根因**：一个函数两个重载，最后的 `MERGE` 调了**没有银行账户分支**的那个
- 有人提议把 ACH 加进检查的排除名单，我**顶回去**，把**数字写下来**
- 队友先落了**止血**；我写 **postmortem** 并做结构性修复
- 结构修复：**单函数**默认参数 + versioned migration **DROP** 旧签名 + 跨 promote 到 fee 的 **e2e** 测试

### R
- 根因在线程里**几分钟**内给出；**重载设计被整个移除**
- 新 **e2e** 覆盖从 promotion 到 fee 生成

### L
- 无法映射的 instrument 必须 **fail loudly**，不能什么都不产出
- NULL 传播是 SQL 属性，规则放在**接缝**

## 追问与回答

- **What did you decide vs. the team?**
  - 判定**检查是对的**、费用真丢；**不加排除名单**；把数字写下来
- **Which part was yours?**
  - **根因**、**postmortem**、重载合并、legacy DROP；止血 PR 是队友的："I owned the RCA and the hardening; the stopgap landed first."
- **Did you backfill?**
  - 不说我 backfill 了；灰度阶段队友说大概不需要
  - 方法论：**fix forward**，必要时 backfill；已被下游消费的错误状态要**更正分录**，不是回滚
- **Why didn't tests catch it?**
  - 只断言**路由**；fixture 用**卡 payload**；pending 行不断言 sub_kind；没有跨 promote→fee 的测试，已补 e2e
- **How do you prevent the class of bug?**
  - **Fail loudly**；修接缝不修调用点；**单函数默认参数**使新分支选不到不完整实现
- **Why delete via versioned migration?**
  - 删掉 `R__` repeatable 文件**不会删已部署对象**
- **How did you rule out other causes?**
  - 时序：每个 age 桶覆盖率都是 0%；stream 绕过：**30 of 30** 行到了 fee staging；对照组 fast ACH 有费用
- **Impact on merchants / money actually lost?**
  - 见待补

## 换个 LP 讲

- **Dive Deep**：切片 → 单笔 → 回溯 → 读两个重载；强调排除时序/stream 的证据
- **Ownership**：不是 assignee，转给自己；止血之后继续 own postmortem、重载合并、DROP；别说止血 PR 是我的
- **Insist on the Highest Standards**：止血只修一例，我要让这类 bug 不可能；单函数 + versioned DROP + e2e
- **Have Backbone**：有人提议排除 ACH，我带着数字说不；只有顶住压力，没有 disagree-and-commit 后半
- **Customer Obsession**：~200 个商户被静默地错误计费；fix forward 需要更正分录；没有客户反馈数据，别编
- **Bias for Action**：转给自己，线程里几分钟给出答案；速度来自对 promote 链路的全局图景
- **Earn Trust**：postmortem 写出我们自己的测试为什么没看见（4 个缺口）

## 待补

- 【待补：缺失费用最终是否 backfill、由谁、花了多久，对商户/收入的实际影响】
- 【待补：提出排除 ACH 的人是什么角色（同级/资深/PM）、你的原话、最后谁拍板（要求「对更资深的人说不并给出数据」）】
- 【待补：postmortem 在哪个会上读过、几个团队参加；其他团队后来有没有采用 e2e 模式或 fail-loudly 规则】
- 【待补：升级句 "I removed the mechanism that allowed this bug class and wrote down why our tests couldn't see it." 对应的证据是否都能说】

<details><summary>逐字稿</summary>

> A daily health check I'd built — "every settled transaction has its Braintree fee" — paged the on-call. I forwarded the page to myself and had the root cause in the thread within a few minutes.
>
> Scoping showed that a hundred percent of the missing fees were bank-account transactions on the new standard-ACH path: about two hundred merchants, roughly ten million dollars a day. The fee calculation builds the pricing category as `'BT_' || payment_instrument_sub_kind`. For these transactions the sub-kind was `NULL`, and in SQL, concatenating `NULL` gives `NULL`, so no category matched and no fee was written — silently, no exception. The reason: one function had two overloads, and the shared final `MERGE` called the one-argument version, which had no bank-account branch, and overwrote the correct value.
>
> There was pressure to add ACH to the check's exclusion list. I put the numbers in writing: the check was right and the fees were really missing. A teammate landed the stopgap first. I owned the root cause, the postmortem, and the hardening: one function with a defaulted parameter, a versioned migration that drops the old signature, and an end-to-end test that spans promotion through fee generation. The rule I pushed: an unmappable instrument must fail loudly, not emit nothing.

</details>
