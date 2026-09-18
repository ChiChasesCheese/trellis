---
title: S9 · Amex 出款延迟事故
aliases:
  - S9
  - 出款延迟事故
  - T+7 SLA
tags:
  - interview/story
  - stack/production
  - collaboration
answers: [Q6, Q10, Q14]
stacks: [TS01, TS08]
status: verified
---

# S9 · Amex 出款延迟事故（事故指挥里的领域权威）

> [!abstract] 一句话
> 一家大型 marketplace 商户报告约 $4M 的 Amex 出款"不见了"，开了正式事故频道；指挥点名我为三位 fix owner 之一。我的两个贡献：① SLA 定论——资深同事说自己没有 US aggregated-Amex SLA 的上下文、defer 给我，我给出"T+7 是内部管线 SLA，且我们只在 Amex 把钱结算到我们账户后才出款"，把预期内的延迟和真正的回归分开；② 回归本身是一次为 EU 合规改 effective-date 的变更把 US 出款日推后一天，我主张在 table function 里加 region conditional 而不是 revert，让 EU / US 语义独立。三天关闭。

## 1. 经过

| 时点 | 事 |
|---|---|
| 事故开 | 商户侧："周末算上像 7 天才出款" |
| SLA 争议 | 同事："I don't have context on US agg-Amex SLAs, I would defer to Chi" → 我："T+7 is our internal pipeline SLA for US; we only disburse after Amex settles the money to our account" |
| 根因 | 指挥通报：6/23 一次 Agg-Amex effective-date 改动（为 EU 合规）把 US 出款日推后 ~1 天；Snowglobe 三位工程师 own 修复：revert + backfill，或在 UDTF 加 US/EU 条件（**preferred, more robust**） |
| 修复 | 由另两位同事落地部署；事故 07-09 关闭 |

## 2. 讲法

- 事故里最贵的不是 bug，是各方对"边界在哪"的误解——先把边界（内部 SLA vs 上游资金到账）讲清，冲突自然消解。
- 多 owner 事故里：**拿你是权威的那一块**，说清、让别人 defer；主张 robust 修法而非 fast 修法；不去挤部署环节。

> [!warning] 证据边界
> - 旧稿说"延迟是上游时序、不是管线故障"——**错**：根因确实是本组的一个 PR。正确说法：SLA 澄清 + 根因是 effective-date 变更 + 我主张 region conditional。
> - 修复由同事部署；说 "one of three owners; my piece was the SLA determination and the fix direction"。
> - 不点商户名（说 "a large marketplace merchant"）、不点同事名。

## 3. English · 首答（60 s）

> A large marketplace merchant reported roughly four million dollars of Amex payouts "missing," and a formal incident channel spun up. The incident commander named me one of three engineers who own the fix. Two contributions. First, the SLA: a senior teammate said he didn't have context on US aggregated-Amex SLAs and deferred to me — I established that T+7 is our internal pipeline SLA and that we only disburse after Amex settles funds to us, which separated expected latency from the real regression. Second, the regression itself: an effective-date change made for EU compliance had shifted US disbursement dates by a day. Reverting was the fast option; the robust fix — which I argued for and the group chose — was a region conditional in the table function so EU and US keep independent semantics. Closed in three days.

## 4. 用在哪

- 回答：[[Answers#Q6]] 影响半径 · [[Answers#Q10]] 跨团队 · [[Answers#Q14]] 冲突
- 场景题：on-call 伙伴出款延迟的前 30 分钟 · 迟到 / 乱序数据
- 技术栈：[[01-system-design|TS01]]（三服务与 T+N 出款）· [[08-observability-oncall|TS08]]
- 相邻：[[S1]]（同一条管线）· [[S4]]

## 5. 证据锚点

Slack 事故频道 2026-07-06 → 07-09（指挥通报、SLA defer 与我的回复）。
