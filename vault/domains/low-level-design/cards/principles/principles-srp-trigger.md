---
id: principles-srp-trigger
node: principles.solid
type: qa
---
## Q
`Invoice` 计算总额、将自己渲染为 PDF、将自己保存到数据库。哪个 SOLID 原则指出这个问题？实际的测试标准是什么？如何重构？

## A
**SRP**。测试标准是*改变的理由数量*，而非"只做一件事"：会计因总额变化，设计因布局变化，DBA 因持久化方式变化——三个利益相关者，一个类。

重构：保持领域逻辑在 `Invoice`；提取 `InvoicePrinter` 和 `InvoiceRepository`。现在每个类恰好因为一个利益相关者而改变。
