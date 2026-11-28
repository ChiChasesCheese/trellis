---
id: hi-c-sd-multi-step-processes-x04-determinism-bug
node: sd.patterns.multi-step-processes.exam
type: qa
step: 4
---
## Q
**多步流程 · 工作流代码里的坑**｜考点 · 必会

同事在 Temporal 工作流函数里直接调用了 `Date.now()`、随机数和一个 HTTP 请求来决定分支，上线后恢复时出现异常行为。为什么？

## A
- **原因：** 恢复靠重放，工作流函数会从头再执行，期望每次做出相同的决定。直接读时钟、随机数、网络返回的值在重放时会不同，决策与历史对不上，可能走到另一个分支。
- **修法：** 网络调用、读数据库放进 Activity，结果记入历史，重放时直接取记录；时间和随机数用 SDK 提供的确定性版本（沙箱化）。
- **对称的要求：** Activity 要幂等，因为崩溃可能让引擎不确定是否完成而重试。
- **要点：** 工作流负责决策且确定，Activity 负责副作用且幂等。
