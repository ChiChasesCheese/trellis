---
id: hl-bs-s1-streams-key
node: behavioral.stories
type: qa
step: 11
---
## Q
结算管线 S1 为什么用多个独立的 stream、复合键里为什么要有 reject indicator、为什么要用 `SYSTEM$STREAM_HAS_DATA` 做门控？

## A
- **为什么分开 stream**：各自有独立的 **offset**，消费者互不阻塞。stream 与写入**不是事务性**的，所以正确性靠**下游 `MERGE` 键**。
- **复合键** = 引用号 + **reject indicator**：同一笔的"已结算"和"被拒"记录可以**共存**，由校验器来裁决。
- **门控**：`SYSTEM$STREAM_HAS_DATA` 保证仓库**不会为空输入而启动**。
