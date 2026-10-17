# S4 · AU Amex 退款费（用一条查询结束 50 条回复）

**A product manager's escalation bounced through three teams for 50 replies; I ended it the same day with one query anyone could re-run.**

## 适用 LP

- 主：**Customer Obsession**、**Dive Deep**、**Earn Trust**
- 副：Are Right A Lot、Have Backbone、Ownership

## 数字

- **50 条回复 / 3 个团队**，线程路由到我之前
- 六个月退款费行数：美国 **~1,079,627**、英国 **294**、澳洲 **0**
- **157** 个 AU 商户；**288 万**笔 AU non-agg Amex 销售
- 所有 AU 商户 `fee_refund_policy` = **partial**（或 none）；退款费逻辑只在 **full** 触发
- 定性："predates the migration"
- 结果：**当天**结束线程，转成功能票 "REFUND_FEE calculation pipeline in Snowglobe"

## S / T / A / R / L

### S
- PM 通过正式 help 流程升级：**澳洲商户**看不到 **Amex 退款费**
- 线程在**三个团队**间弹了约 **50 条回复**

### T
- 作为**熟悉该领域**的人被路由到我；我 own 的是**答案**，不是工单

### A
- **拉数据**而不是看组织架构：六个月按国家数退款费行
- 美国**百万级**，澳洲 **0**，涉及 ~**150** 个商户
- 根因在**配置**：AU 商户的 `fee_refund_policy` 都是 **partial**，逻辑只在 **full** 触发
- 证明**早于迁移**，不是我们引入的回归
- 写结论并附**原始查询**，PM 和另一团队可**自己复跑**
- 第二个无关的费用种类：我说 **"not sure yet"**，给**分层假设**，资深工程师确认

### R
- 线程**当天结束**；变成跟踪中的**功能票**

### L
- 分歧其实是**知识不对称**时，给所有人**同一份证据**，不争归属

## 追问与回答

- **How did you know it wasn't a regression?**
  - 上游**出款服务**从来没为 AU direct-Amex 发过退款费；迁移里变的只有**报表**
- **Why did you pull data rather than discuss?**
  - 争论源于领域知识不对称；数据让所有人**当场可验证**
- **What was the second issue?**
  - AU-only `refund` 费用种类；我说**不确定**，给分层假设和验证方法；资深同事确认
- **What did you do for the merchants in the meantime?**
  - 见待补
- **What if the data had contradicted your guess?**
  - 方法不变：结论由**查询**给出，不由我给出
- **Who owns the new feature? How big is the money?**
  - 见待补

## 换个 LP 讲

- **Customer Obsession**：AU 商户没拿到应有的退款费，三个团队没人负责查清；回到证据，变成正式功能票；没有商户补偿数字，别编
- **Dive Deep**：不读组织架构读数据，百万行 vs 零；按国家拉数 → `fee_refund_policy` → 证明早于迁移
- **Earn Trust**：把原始查询放进文档让对方自己核对；对第二个问题坦承 not sure + 计划
- **Are Right, A Lot**：说 "I wasn't sure yet" 并给出可能出错的假设，被资深同事确认；不说「我从不错」
- **Have Backbone**：三团队互相指，我带数字说是配置而且早于我们；不是 disagree-and-commit
- **Ownership**：不是我的工单，我 own 答案；说 "routed to me as the person who knows that domain"，不说「PM 让我做」

## 待补

- 【待补：写完后有没有把「按国家/配置拉数」的查询存成团队 runbook/看板，下次类似问题能自助】
- 【待补：是否有临时补偿/手工修复；没有就如实说「没有，已立功能票」】
- 【待补：你最初的假设是什么、被数据推翻了哪一半（若有）】
- 【待补：feature ticket 的 owner 与排期，后来是否上线】
- 【待补：AU 漏掉的退款费金额量级】
- 【待补：线程里谁最初主张「是迁移的锅」，你如何不得罪人地纠正】

<details><summary>逐字稿</summary>

> A product manager escalated through our formal help process: Australian merchants weren't seeing Amex refund fees. It bounced across three teams for about fifty replies before it was routed to me as the person who knows that domain.
>
> I pulled the data instead of the org chart. Over six months there were more than a million refund-fee rows in the US and zero in Australia, across about a hundred and fifty merchants. The root cause was configuration, not code: every Australian merchant's pricing schedule had the refund policy set to `partial`, and the refund-fee logic only fires on `full`. I also showed it predated our platform migration, so it wasn't a regression we introduced.
>
> I wrote it up with the exact query so the PM and the other team could re-run it themselves. It ended the thread the same day and became a tracked feature to build the refund-fee pipeline properly. In the same thread a second, unrelated fee kind came up; I said I wasn't sure, laid out a layered hypothesis, and a senior engineer confirmed it. I'd rather say "not sure yet" with a plan than guess.

</details>
