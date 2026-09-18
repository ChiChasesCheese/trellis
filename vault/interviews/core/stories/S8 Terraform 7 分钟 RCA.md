---
title: S8 · Terraform grant-ownership 7 分钟 RCA
aliases:
  - S8
  - Terraform RCA
  - outbound_privileges
tags:
  - interview/story
  - stack/terraform
  - stack/production
answers: [Q15]
stacks: [TS04, TS08]
status: verified
---

# S8 · Terraform grant-ownership 7 分钟 RCA（压力下 debug · unblock · 主动指出下一个雷）

> [!abstract] 一句话
> 基础设施仓库的发布在 QA 挂了：`GRANT OWNERSHIP` 被 Snowflake 拒绝，因为 reviewer 角色已持有依赖的 `USAGE` 授权。被点名调查的是别人，我只是被 cc；7 分钟后我贴出根因（ownership 资源没设 `outbound_privileges`）、修法（`= "REVOKE"`）和对相邻模块的核查，问了一句可否推 PR，QA → pre-prod → prod 当天部署完。**事后**我扫了全仓库：79 个同类资源里 42 个缺该参数——多数是无害的 `future_*` 变体，但另一个模块里有两个与出事的那个形状完全一样、尚未触发的风险，我标出来了。

## 1. 机制

- Snowflake 的 ownership 转移要求先撤销目标对象上其它角色持有的依赖授权；Terraform provider 的 `snowflake_grant_ownership` 用 `outbound_privileges = "REVOKE" | "COPY"` 表达这一步，不设就会在 apply 时被拒。
- Terraform 没有事务：apply 到一半失败，部分资源已建、state 部分更新，需要重跑收敛——所以危险变更要拆小、可重入。
- 重命名资源默认删了重建（`moved` block / `state mv`）——最容易造成生产事故的"无害"操作。

## 2. senior 的部分

- 快不是天赋，是对整个 repo grant 结构有全局图景。
- "修完这一次"和"消灭这一类"是两件事：我修了 fee-anomalies 模块，又指出 `scheme_fees` 模块两处同类风险未修——**主动给出这个数字比被问出来强**。

> [!warning] 证据边界
> 面试时我曾说 "the only resource in the whole repo missing it"——**不成立**（42/79 缺）。当时我核查的是指定的几个模块，这个较窄的说法是真的。现在的说法："I checked the neighboring modules that day; afterwards I scanned the whole repo and found dozens missing it, mostly harmless future grants, but two real ones in another module that haven't fired yet."

## 3. English · 首答（60 s）

> A release of our Snowflake infrastructure repo failed in QA: `GRANT OWNERSHIP` on a database was rejected because a reviewer role already held a dependent `USAGE` grant. Someone else was named to investigate; I was cc'd. Seven minutes later I'd posted the root cause — the ownership resource didn't set `outbound_privileges`, so Terraform tried to transfer ownership without revoking dependents — the fix, `outbound_privileges = "REVOKE"`, and a check of the neighboring modules for the same omission. I asked for permission to push, the PR went in, and QA, pre-prod and prod deployed that afternoon.
>
> The senior part is what I found afterward: scanning the whole repo, dozens of ownership resources lack the parameter — most are `future_*` grants where it's harmless — but two in another module are the exact same shape as the one that blew up and haven't fired yet. I flagged them; I'd rather own "here's the next one" than just the one that paged.

## 4. 用在哪

- 回答：[[Answers#Q15]] unblock / go-to
- 亲历题：shipping under a hard deadline · unblocking someone under pressure
- 技术栈：[[04-terraform-iac|TS04]] · [[08-observability-oncall|TS08]]
- 相邻：[[S3]]（另一次 RCA）· [[S6]]（同一项目）

## 5. 证据锚点

Slack #treasury-services-releases 2026-08-13；PR snowglobe-terraform #1326；全仓库扫描见本机 `raw/repo-snowglobe-terraform.md` §5。
