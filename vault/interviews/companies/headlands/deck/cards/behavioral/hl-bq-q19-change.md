---
id: hl-bq-q19-change
node: behavioral.question-bank
type: qa
step: 39
---
## Q
有哪个设计决定你会改？（45 秒）
A design decision you'd change.

## A
故事：S1 / S7。

- **S1**：**偏移表重复了六次** → 改成**配置表 + 一个通用解析器**。
- **S7**：V1 从一个**共享 schema** 克隆，它的状态取决于**最后谁迁移过**；V2 从**已部署的 commit** 推导。
- **Pattern**：让系统的**输入**变成**一个确定性的东西**。
