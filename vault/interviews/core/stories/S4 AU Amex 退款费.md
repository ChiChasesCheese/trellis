---
title: S4 · AU Amex 退款费（跨团队，用数据结束争论）
aliases:
  - S4
  - AU Amex refund
tags:
  - interview/story
  - stack/sql
  - collaboration
answers: [Q6, Q14, Q15]
stacks: [TS09]
status: verified
---

# S4 · AU Amex 退款费（跨团队 · 用一条查询结束 50 条回复）

> [!abstract] 一句话
> PM 走正式求助流程："澳洲商户看不到 Amex 退款费"，三个团队 50 条回复后路由到我。我不查组织架构查数据：六个月内美国 ~108 万行退款费、澳洲 0 行、跨 157 个商户；根因是配置不是代码——所有 AU 商户的 `fee_refund_policy = partial`，而退款费逻辑只在 `full` 时触发；并且这早于我们的平台迁移。写成带查询的结论让对方自己复跑，当天结束讨论，变成一张正式的功能票。

## 1. 经过

1. 正式 "Request Help" 表单 → 被点名（"你有 AU Amex 交易和 BT fee 的上下文"）。
2. 拉数：`NON_AGGREGATED_TRANSACTION_FEE_REFUND` 按国家六个月：USA 1,079,627 · GBR 294 · AUS **0**；157 个 AU 商户、288 万笔 AU non-agg Amex sales。
3. 根因：每个 AU 商户的定价计划 `fee_refund_policy` 是 `partial`（或 none），从来不是 `full`；退款费只在 `full` 时生成。
4. 定性：**predates the migration**——上游出款服务从来没为 AU direct-Amex 发过退款费，变的只是报表口径。不是我们引入的回归。
5. 写清根因 + 可复跑的 SQL → 同一线程里第二个不相关问题（AU-only 的 `refund` fee kind）我说"不确定"，给分层假设，资深同事确认"Chi is right"。
6. 结果：新功能票 "REFUND_FEE calculation pipeline in Snowglobe"。

## 2. 为什么它是好故事

- 冲突解法不是协调会，是**把争论从"谁的锅"拉回到一份所有人都能复跑的证据**。
- "predates the migration" 这一句把跨团队的指责变成共同事实。
- 第二个问题上敢说"not sure yet"并给出验证计划——比硬答更 senior。

> [!warning] 证据边界
> 不点名同事；不说 "PM 让我做"，说 "routed to me as the person who knows that domain"。

## 3. English · 首答（60 s）

> A product manager escalated through our formal help process: Australian merchants weren't seeing Amex refund fees. It bounced across three teams in a fifty-reply thread before it was routed to me as the person who knows that domain.
>
> I pulled the data instead of the org chart: over a million refund-fee rows in the US over six months, zero in Australia, across about a hundred and fifty merchants. The root cause was configuration, not code — every AU merchant's pricing schedule had `fee_refund_policy = partial`, and the refund-fee logic only fires on `full`. I also showed it predated our platform migration, so it wasn't a regression we'd introduced.
>
> I wrote it up with the exact query so the PM and the other team could re-run it themselves. It ended the thread the same day and became a tracked feature to build the refund-fee pipeline properly. Giving everyone the same evidence beat arguing about ownership.

**追问**：*"A second, unrelated fee kind surfaced in the same thread — I said I wasn't certain, laid out a layered hypothesis, and a senior engineer confirmed it. I'd rather say 'not sure yet' with a plan than guess."*

## 4. 用在哪

- 回答：[[Answers#Q6]] 影响半径 · [[Answers#Q14]] 意见冲突 · [[Answers#Q15]] go-to person
- 场景题：两个系统对不上一个数字
- 相邻：[[S9]]（另一种跨团队：事故指挥）· [[S10]]（同为"用查询定案"）

## 5. 证据锚点

Slack #service-pricing 2026-08-03 → 08-17；Jira DTBTTFOUND-3269 / 3310。
