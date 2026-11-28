---
id: hi-c-lld-design-principles-x09-over-split
node: lld.in-a-hurry.design-principles.exam
type: qa
step: 9
---
## Q
**设计原则 · SRP 拆过头**｜考点 · 追问

面试里你把 `Report` 拆成了 `ContentGenerator`、`PdfFormatter`、`FileWriter`、`ReportFacade`，面试官说"太碎了"。怎么判断拆到哪合适？

## A
- **判据：** "改动的理由"是否不同，而不是方法个数
- **该拆：** PDF 库和存储介质确实会独立变化
- **可不拆：** 题目只要求生成文本，一个类足够，拆了违反 KISS
- **说法：** 先写简单版，说明如果出现第二种输出格式，就把格式化拆出来
- **信号：** 拆出来的类只有一个方法、被一个调用方使用，往往拆早了
