---
id: mlp-hm-fail-pressure-rca
node: hm.failure
type: qa
step: 2
---
## Q
**压力下的 7 分钟定位**｜经理面与行为面

“Tell me about a time you had to debug under pressure or hit a hard deadline.”

## A
问的是压力下的速度和判断：基础设施仓库的发布挂在 QA，团队在等。

- **情境：** 发布在 QA 失败，`GRANT OWNERSHIP` 被 Snowflake 拒绝，因为 reviewer 角色已持有依赖的 `USAGE` 授权。被点名调查的是别人，你只是被抄送。
- **行动：** 7 分钟后你贴出根因、修法 `outbound_privileges = "REVOKE"`，以及对相邻模块的检查，并问一句能不能推 PR。当天 QA、预生产、生产都部署完。
- **事后：** 扫描整个仓库，79 个同类资源里 42 个缺该参数，多数无害，但另一个模块有两个与出事那个完全同形状的风险，你主动标出。
- **要点：** 修这一次和消灭这一类是两件事；主动说“下一个雷在这里”比被问出来强。
- **背景知识：** Terraform 没有事务，apply 到一半失败会留下部分状态，所以危险变更要拆小、可重入。

**英文答法。**
- A release of our infra repo failed in QA: `GRANT OWNERSHIP` was **rejected** because another role already held a dependent grant.
- Someone else was named to investigate; **seven minutes later** I'd posted the **root cause, the fix and a check of neighboring modules**, and asked to push.
- QA, pre-prod and prod **deployed that afternoon**.
- Then I scanned the whole repo and flagged **two real look-alikes** in another module — I'd rather own "here's the next one" than just the one that paged.

**追问。**
- **You said you checked the whole repo?** On the day I checked the neighboring modules; the full scan came afterwards and found dozens missing it, mostly harmless future grants.
- **How did you get it merged?** I asked for permission to push in the same message; the PR went in and the release continued.
- **What does Terraform's lack of transactions mean?** A failed apply leaves partial state, so risky changes should be small and re-runnable.
