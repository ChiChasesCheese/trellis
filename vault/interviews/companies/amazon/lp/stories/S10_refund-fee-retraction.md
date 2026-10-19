# 退款费 billing-terms 复盘（推翻自己的数字）

**My first blast-radius query said 196K rows; before anyone acted I found the predicate was wrong, retracted it myself, and the real number was 21,923.**

## 适用 LP

- 主：**Earn Trust**、**Dive Deep**、**Are Right, A Lot**
- 副：Insist on the Highest Standards、Customer Obsession、Ownership

## 数字

- 第一版：**196,274 行 / 61 商户 / ~$11,123**（谓词：credit 计划 monthly ∧ 费用创建当天生效计划 daily/net ∧ 生成的 billing_terms 仍 MONTHLY）
- 修正（加 `ps_curr.created_at <= bf.created_at`）：**21,923 行 / 10,330 credits / 30 商户 / $5,854.52**
- 1,062 个切到 NET 的美国商户里只有 **5 个**产生 bug 费用
- 那家电商：**216 行**、延迟 **214 天**
- 上游"计划写入滞后" **1 小时 32 分**
- $ 口径：`SUM(ABS(amount))/100`
- 回填：TEMU/SHEIN **191,191** 笔 sales → **382,382** fee 行

## S / T / A / R / L

### S
- 一家大型电商商户切到 **net settlement**
- 部分**退款费**带着旧的 **monthly** billing terms

### T
- 我 own **爆炸半径估算**和**根因**
- 修复范围必须按**正确的数字**，不能按错谓词

### A
- 写估算查询：**约 20 万行费用、六十个商户**
- **没人行动之前**重读自己的谓词，发现**错了**
- 它没检查新计划在**费用创建时已存在**；很多是**几个月后回填**的，写入时是对的
- **加上该条件**重跑，真实范围小得多
- **根因**：退款费路径**复制了 credit 的历史计划 ID**，没有在费用创建时重新解析
- 另发现**上游脆弱点**：计划在 stream 给当天 credit 盖章**一个半小时之后**才写入

### R
- 真实范围：**~22K 行、30 商户、不到 $6K**，而不是 200K 和 60
- **一个修法同时覆盖**两个脆弱点：费用创建时解析生效计划

### L
- 宁可**公开撤回自己的数字**，也不按错谓词定补救范围
- 每个结论配一条**可重跑的查询**；爆炸半径谓词必须检查**时间有效性**

## 追问与回答

- **How did you discover the predicate was wrong?**
  - 见待补
- **Who had seen your first number?**
  - 见待补
- **Why is the blast radius bounded?**
  - 切换后新 credit 自动拿到 **NET 计划 ID**；只有**切换前积压、切换后才跑**的商户受影响
- **How do you fix it?**
  - 费用创建时调 **`EFFECTIVE_PRICING_SCHEDULE(maid, date)`**；**不复制** credit 的历史计划 ID
- **What about the upstream lag?**
  - 函数按查询时**物理存在**的计划解析；批量铺开时滞后可能是**系统性**的；创建时重新解析**两者都缓解**
- **How do you know $5,854.52 is right?**
  - 口径 **`SUM(ABS(amount))/100`**；SQL 附录在复盘文档里
- **What changed in how you work?**
  - **每个结论一条可重跑查询**；爆炸半径谓词检查**时间有效性**

## 换个 LP 讲

- **Earn Trust**：在任何人据此行动前公开撤回；两版查询并排；是我自己发现的，不要说成「被人抓到」
- **Dive Deep**：196K 和 22K 的差别只是一个关于"行是何时创建"的条件；谓词、时间有效性、1h32m 滞后
- **Are Right, A Lot**：把自己的查询当作要 disconfirm 的假设；重审谓词，先排除美国特判，`GET_BILLING_TERMS` 数据驱动
- **Insist on the Highest Standards**：一个修法覆盖下游和上游两个脆弱点：费用创建时重新解析生效计划
- **Customer Obsession**：三十个商户按错误条款计费；商户侧影响与回填
- **Ownership**：我 own 估算和根因，并跟到回填 PR（191,191 → 382,382）；不点名商户

## 待补

- 【待补：修复是否已上线】
- 【待补：触发点，比如抽样某行发现计划是几个月后回填的；被问「错的假设」需要真实细节】
- 【待补：196K 是否已发给他人/进入 ticket，「在任何人据此行动之前」需要你能支持的事实】
- 【待补：复盘后团队是否多了「sizing 查询必须带时间有效性条件」的 checklist / 模板】
- 【待补：这份复盘谁读了、基于它做了什么决定（回填范围、优先级）】

<details><summary>逐字稿</summary>

> After a large e-commerce merchant moved to net settlement, some refund fees came out tagged with the old monthly billing terms. My first blast-radius query said about two hundred thousand fee rows across sixty merchants. Before anyone acted on it, I re-examined the predicate and found it was wrong: it didn't check that the new pricing schedule existed at the time the fee was created. Many of those rows had schedules backfilled months later and were correct when written. Adding that condition took the real scope to about twenty-two thousand rows, thirty merchants, under six thousand dollars.
>
> The root cause was that the refund-fee path copied the credit's historical pricing-schedule ID instead of resolving the effective schedule at fee-creation time. Along the way I found a second, upstream fragility: a schedule written to the database an hour and a half after the transaction stream had already stamped that day's credits. One fix covers both. I'd rather retract my own number in public than have a remediation sized off a bad predicate.

</details>
