---
id: hl-bs-s6-followups
node: behavioral.stories
type: qa
step: 33
---
## Q
被追问 S6：你剖析过吗？逐行 numpy 为什么慢？QA 为什么看不出？下推（pushdown）总是更快吗？第二阶段值不值得怎么定？
Did you profile it? Why couldn't QA show it? Is pushdown always faster?

## A
- **Did you profile it?** **没有**，它从没在规模上跑过；我会先量每行延迟，再分 CPU 与数据传输，再看批处理。
- **Why is per-row numpy slow?** 每行**调用开销** + **数据搬出仓库**；集合式查询是原地**一次扫描**。
- **Why couldn't QA show it?** 6 个商户藏住了**每行的固定成本**。
- **Is pushdown always faster?** 只有逻辑能写成**集合运算**且数据已在仓库里才行；神经网络前向不能，所以才有第二阶段。
- **Phase 2 worth it?** **业务驱动** + 影子模式下**测得的精度**。
