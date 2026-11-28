---
id: hi-c-lld-logging-service-n08-destination-options
node: lld.problem-breakdowns.logging-service.notes
type: qa
step: 8
---
## Q
**日志库 · Destination 的三种写法**｜摘要 · 必会

`Destination` 有三种常见设计：按类型分支、继承加模板方法、组合 Sink。各自的毛病是什么，选哪个？

## A
| 方案 | 做法 | 问题 |
|---|---|---|
| 单类按类型分支 | 一个类有 `type` 字段，`write` 里 if/else | 每加一种目标就多一个分支，且多数字段（文件路径、套接字地址）对大多数实例是空的；违反开闭原则（OCP） |
| 继承 + 模板方法 | 基类的 `write` 做过滤、格式化、加锁，子类只实现 `do_write` | 保证了"过滤和格式化只写一处"，但子类与父类几乎不共享数据，继承理由薄；想包装缓冲、重试、双写时，只能继续子类化，层次越叠越深 |
| 组合 Sink（选这个） | `Destination(formatter, min_level, sink)` 是具体类，写出委托给 `Sink` | 多一个接口，两个输出目标时略重 |

- **选组合的理由：** 保留了"不变量只写一处"的好处，没有层次，新目标就是新 `Sink`，测试时传一个记录调用的假 sink。真实的日志库都收敛到这个形状（Log4j 把布局和输出流分开，Python 的 logging 把 Formatter 和 Handler 分开）。
- **Destination 保持具体类：** 过滤、格式化、加锁、委托只有一种合理形状，变化在 Sink 和 Formatter 后面；为单个实现再加 `IDestination` 是为抽象而抽象。
- **继承也能得分：** 关键是说清为什么没选另一个。
