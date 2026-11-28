---
id: hi-c-lld-logging-service-n17-ext-hierarchy
node: lld.problem-breakdowns.logging-service.notes
type: qa
step: 18
---
## Q
**日志库 · 扩展：层级命名 logger**｜摘要 · 追问

真实框架里 `getLogger("com.app.service.payments")` 会继承父级配置。怎么在现有设计上加这个能力？

## A
- **做法：** `Logger` 加 `name` 和 `parent` 指针，前面加一个 `LoggerFactory`：它持有"名字到 logger"的注册表，按点分前缀找父级，没有就退到根。有效级别和有效目的地在自己没设置时沿父链向上查。
- **缓存有效级别：** `log()` 是系统里最热的路径，不能每次沿父链走一遍。真实框架把有效级别缓存在每个 logger 上，配置变化时使缓存失效。
- **工厂是刻意的全局：** 注册表的意义就是同一个名字在代码库任何位置拿到的是同一个实例，这是少见的、共享应用状态本身就是需求的情况，不是随手用全局。
- **效果：** 负责 `com.app.service` 的团队设一次阈值，下面所有子 logger 自动继承，除非自己覆盖。
