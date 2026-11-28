---
id: hi-c-sd-multi-step-processes-n08-how-durable-execution
node: sd.patterns.multi-step-processes.notes
type: qa
step: 8
---
## Q
**多步流程 · 持久化执行的工作原理**｜摘要 · 必会

Temporal 里工作流（Workflow）和活动（Activity）分别是什么？为什么要求确定性和幂等？崩溃后怎么恢复？

## A
- **分工：** Workflow 是高层流程，相当于菜谱（步骤顺序和之间的决策）；Activity 是其中一步，真正接触外部世界，如调服务、扣款、发邮件。
- **工作流代码必须确定性**（deterministic）： 同样的输入和历史总是做同样的决定。时间戳、随机数由 SDK 沙箱化保证重放一致；网络调用、读数据库这类不确定的操作必须放进 Activity。
- **Activity 必须幂等**（idempotent）： 引擎不会重试已报告成功的 Activity，但崩溃可能让引擎不确定它是否完成，这时会重试，幂等让重试无害。
- **为什么确定性：** 恢复靠重放（replay）。每个 Activity 结果记入历史库，工作流进程崩溃后，另一个进程从头重新执行 Workflow 函数；遇到已经执行过的 Activity，历史直接返回记录的结果而不再调用。无副作用，执行精确落在中断处。
- **例子：** 付款、预留库存都已记录，服务器死亡，新 worker 重放时前两步直接取历史，到 `shipOrder` 发现无记录才真正执行：客户只被扣一次款。
- **2026 亮点：** 持久化执行也可以做成库而不是服务：DBOS 这类库把每个 workflow 的状态和每个已完成 step 的输出存成 Postgres 的行，重启后重新执行 workflow 函数，已落库的 step 直接返回结果，确定性要求和 Temporal 相同。已经有 Postgres、不想运维 Temporal 集群时合适；代价是状态和吞吐都绑在那个 Postgres 上（队列也由它支撑），没有 Temporal 那样独立的服务端和调度层，规模很大时要靠分片 Postgres。
