---
id: principles-srp-trigger
node: principles.solid
type: qa
step: 2
---
## Q
`Invoice` 既计算总额，又把自己渲染成 PDF，又把自己存进数据库。这违反了哪条 SOLID 原则？实际的判断标准是什么？怎么重构？

## A
**单一职责原则（Single Responsibility Principle，SRP）**。判断标准是*改变的理由数量*，而不是字面上的"只做一件事"：会计因为总额算法变化要改它，设计师因为 PDF 排版变化要改它，DBA 因为存储方式变化要改它——三个不相关的利益相关者，同一个类。

重构：领域逻辑留在 `Invoice`；把渲染和持久化分别提取成 `InvoicePrinter` 和 `InvoiceRepository`。现在每个类恰好只因为一个利益相关者的变化而改变。
