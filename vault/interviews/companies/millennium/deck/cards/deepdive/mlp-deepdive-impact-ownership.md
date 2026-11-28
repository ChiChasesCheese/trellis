---
id: mlp-deepdive-impact-ownership
node: deepdive.impact
type: qa
step: 2
---
## Q
**哪部分是你的**｜项目深挖

“What exactly did you do versus the team?”

## A
深挖里最常见的陷阱是被问“这是你一个人做的吗”。每个项目准备好一句边界。主动说清边界，比被问出来强。

- **Amex 管线：** 接手时只有一张表的 stub，拓扑起往后都是你的，包括设计文档；任期内最大的 PR 是它。它是接收侧的 Snowflake 原生替代，原来的 Amex 结算逻辑在 Rails 出款服务里；不要说成你迁移了出款的脚本。
- **净额结算：** 项目整体的负责人不是你；你负责费用侧，interchange 这一条线。
- **NULL 事故：** 止血 PR 是同事先合的；根因、复盘、重载整合和删除旧签名是你的。
- **出款延迟：** 三位负责人之一；SLA 结论和修法方向是你的，部署是同事。
- **schema pool：** 个人仓库，你建的，团队采用。
- **质检框架的商户级：** 设计和评审完成，在一个数据域验证；整体铺开还没做。
- **实习：** broker 和代理是平台团队的；你的在消费、落库和校验侧。

**英文答法。**
- I **own the fee side**, the interchange track, inside the net-settlement program; I'm not the program's sole owner.
- On the ACH incident, a teammate's **stopgap landed first**; I owned **the RCA and the hardening**.
- On the payout delay I was **one of three owners**: my piece was the **SLA determination and the fix direction**.
- The schema pool lives in **my own repo**: I built it, the team adopted it.

**追问。**
- **Did you migrate the payout scripts?** No; my pipeline is the receiving-side Snowflake-native replacement for the Amex settlement logic that lived in the Rails payout service.
