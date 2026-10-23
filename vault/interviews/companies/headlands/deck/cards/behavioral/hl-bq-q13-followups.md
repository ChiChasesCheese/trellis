---
id: hl-bq-q13-followups
node: behavioral.question-bank
type: qa
step: 28
---
## Q
"性能问题"之后的追问：你剖析过吗？为什么逐行 numpy 慢？怎么决定第二阶段值不值得做？
Did you profile it? Why is per-row numpy slow here? How do you decide Phase 2 is worth it?

## A
- **Did you profile it?** **没有**，它从没在规模上跑过；我会先量**每行延迟**，再分 **CPU 与数据传输**。
- **Why is per-row numpy slow here?** 每行的**调用开销**加上**数据搬出仓库**；集合式查询是原地**一次扫描**。
- **How decide Phase 2 is worth it?** 需要**业务驱动** + 影子模式下**测得的精度**。
