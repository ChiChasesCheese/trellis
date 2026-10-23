---
id: hl-bs-s5-window
node: behavioral.stories
type: qa
step: 25
---
## Q
S5 里为什么要在合并的 `ON` 上加一个月窗口？它的代价是什么？

## A
- **为什么**：staging 表只增不减，用等值 `ON` 会扫描**全部历史**；加一个月窗口后，**zone map** 能剪枝，**扫描成本保持恒定**。
- **代价**：一条记录在**一个月之后**被重新处理，会**绕过去重**；我把这个盲区**写在子句旁边**。

如何证明剪枝有效：读**查询剖析**（partitions scanned vs total）。【待补：是否真的看过；没有就说 "I reasoned it from the clustering"】——这是设计推理，不是测量。
