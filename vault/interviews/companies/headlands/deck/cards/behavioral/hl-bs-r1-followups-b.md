---
id: hl-bs-r1-followups-b
node: behavioral.stories
type: qa
step: 7
---
## Q
被追问个人研究平台 R1：paper trading 和回测的差距？怎么加速引擎？它能扩展到我们这样的公司吗？
Paper vs backtest gap? How would you speed up the engine? Would it scale to a firm like this?

## A
- **Paper vs backtest gap?** 差在**成交、延迟、成本、冲击**。【待补：真实偏差，或 "not enough sample yet"】
- **How would you speed up the engine?** **先剖析**，检查**列式布局**，**向量化**，避免逐行 Python。（这是思路，不是我做过的事。）
- **Would it scale to a firm like this?** 不能；真实平台在**数据量、分布式、可靠性**上大得多，这正是我想学的那一层。
