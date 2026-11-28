---
id: hi-c-sd-temporal-n09-outbox
node: sd.deep-dives.temporal.notes
type: qa
step: 14
---
## Q
**Temporal · 状态更新与派发任务如何不被崩溃拆开**｜摘要 · 追问

Activity 完成后，更新状态与"让 Workflow 再运行"这两件事怎么保证不丢？计时器怎么做？

## A
- **风险：** 状态已提交，但还没来得及通知 Matching 就崩溃，Workflow 就不会再被调度。
- **做法：** History Service 在同一次提交里持久化更新后的事件历史、可变状态，以及一个内部的持久任务——Transfer Task。后台处理器随后把这个任务送给 Matching，Matching 让对应的 Workflow Task 对 worker 可用。
- **这就是事务性发件箱**（transactional outbox）：提交状态之后即使崩溃，也知道这份后续工作最终需要被派发。
- **计时器用同样的机制：** 计时器是与 History 分片关联的内部 Timer Task，触发时间到了，Temporal 记录计时器触发并创建需要让 Workflow 再次运行的工作。
