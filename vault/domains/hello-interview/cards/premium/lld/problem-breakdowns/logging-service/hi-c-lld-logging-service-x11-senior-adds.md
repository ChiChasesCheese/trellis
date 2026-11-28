---
id: hi-c-lld-logging-service-x11-senior-adds
node: lld.problem-breakdowns.logging-service.exam
type: qa
step: 7
---
## Q
**日志库 · 高级候选人比中级多做了什么**｜考点 · 必会

两个人都做出了 Logger、Record、Formatter、Destination。高级答案多出的五个点是什么？

## A
- **主动比较继承和组合：** 不等被问，列出分支、模板方法、Sink 组合，选后者并说明理由。
- **说明依赖方向：** 高层的 `Destination` 依赖 `Sink`、`Formatter` 抽象，不依赖具体类。
- **时间戳和线程名入口取一次：** 并解释为什么不在目的地取。
- **并发上有立场：** 每目的地一把锁、格式化在锁外，并给出全局锁错在哪里的具体场景（慢磁盘拖住控制台）。
- **失败处理：** 吞掉异常保证不崩调用方，再写 stderr 诊断避免静默，并提到诊断要限量。
- **早完成时能讲：** 异步队列的溢出策略和关闭流程，层级 logger 的注册表和缓存。
