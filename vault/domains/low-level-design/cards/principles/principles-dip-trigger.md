---
id: principles-dip-trigger
node: principles.solid
type: qa
---
## Q
```java
class ReportService {
  private final MySqlReportStore store = new MySqlReportStore();
}
```
What does DIP say is wrong, what's the refactor, and how does DIP differ from dependency injection?

## A
High-level policy (`ReportService`) depends on a concrete low-level detail. DIP: both should depend on an abstraction shaped by the policy's needs — a `ReportStore` interface — so the dependency arrow points *toward* the policy.

Refactor: accept `ReportStore` via the constructor. DIP is the design rule (who depends on whom); **DI is merely the mechanism** that satisfies it by passing the concrete in from outside.

## Q zh
什么时候你知道有些代码需要依赖反转？

## A zh
触发器：
- 你看到一个高级模块（业务逻辑）导入一个低级模块（基础设施、框架）
- 所有的变化都强制改变依赖于它的所有东西
- 你在测试中需要做很多工作来隔离一个类：创建真实的数据库连接、调用外部 API 等。

