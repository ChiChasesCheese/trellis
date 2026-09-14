---
id: distributed-clock-error-sources
node: distributed.time.clocks
type: qa
---
## Q
Every server in your fleet runs NTP, so an engineer assumes timestamps are accurate "to within a millisecond or so." Walk through the error sources that make tens of milliseconds — or unbounded error — the honest assumption.

## A
- **Quartz drift between syncs**: cheap oscillators drift on the order of tens to hundreds of parts per million with temperature — at 200 ppm that's ~17 s/day; even between 30-second NTP polls the clock wanders several ms.
- **NTP's floor is the network**: it estimates offset assuming symmetric path delay; congestion or asymmetric routes translate directly into offset error. A few ms on a LAN, tens of ms over WAN, worse under load.
- **Corrections are ugly**: large offsets are fixed by **stepping** the clock (a jump, possibly backwards); a wrong-by-minutes node may also *refuse* to sync (panic threshold), or the NTP server itself may be wrong/firewalled — misconfiguration commonly goes unnoticed for months because nothing crashes.
- **Virtualization and pauses**: a VM migration or suspend freezes the guest clock until the hypervisor snaps it forward.
- **Leap seconds**: a 61-second minute has crashed real systems; providers now hide it by **smearing** the extra second over hours — during which everyone's clocks are deliberately wrong and *differently* wrong across providers.

Conclusion: without measuring your own infrastructure you cannot defend any bound — which is why timestamp order is never trusted as event order.

## Q zh
你的机群每台服务器都跑着 NTP，于是工程师假设时间戳"精确到一毫秒左右"。逐项说明那些让"数十毫秒——甚至无界误差"才是诚实假设的误差来源。

## A zh
- **两次同步之间的石英漂移**：廉价振荡器随温度漂移几十到几百 ppm——按 200 ppm 算约合每天 ~17 s；即便 NTP 每 30 秒轮询一次，期间时钟也会游走几个毫秒。
- **NTP 的下限是网络**：它在"路径延迟对称"的假设下估算偏移；拥塞或不对称路由会直接变成偏移误差。局域网内几毫秒，广域网几十毫秒，高负载时更糟。
- **纠偏很难看**：偏移过大时靠**跳变（stepping）**修正——时钟跳跃，甚至倒退；错了几分钟的节点还可能*拒绝*同步（panic 阈值），NTP 服务器本身也可能错误或被防火墙拦住——这类错配常常几个月无人发现，因为什么都没崩。
- **虚拟化与暂停**：VM 迁移或挂起会冻结客户机时钟，直到 hypervisor 把它猛拽回来。
- **闰秒**：61 秒的一分钟真的搞垮过系统；服务商如今用**拉伸（smearing）**把多出的一秒摊到数小时里——期间所有时钟都是故意不准的，而且不同服务商各错各的。
- 结论：不实测你自己的基础设施，任何误差上界都无从辩护——这正是时间戳顺序从不被当作事件顺序的原因。
