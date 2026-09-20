---
id: kafka-connect-smt-insertheader-lineage-example
node: connect.smt
type: qa
step: 5
source: kafka-2e
---
## Q
如果想给某个连接器同步过来的每一条记录都打上「这条数据来自哪个连接器」的标记，方便后续做数据溯源审计，同时又不想改动原始的业务字段，应该用哪个 SMT？它是往哪里加信息的？

## A
应该用 `InsertHeader`：它会在每条消息的**消息头（header，独立于消息键值的一块元数据区域）**里插入一个固定的字符串，比如把消息头字段设为「MessageSource」、值设为连接器的名字。因为信息是加在消息头而不是消息本身的键或值里，原始的业务数据结构完全不受影响，下游想要按需读取这个溯源标记，也可以在消费时专门去查消息头，两者互不干扰。
