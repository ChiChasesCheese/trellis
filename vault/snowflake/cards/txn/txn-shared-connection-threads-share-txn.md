---
id: txn-shared-connection-threads-share-txn
node: txn.acid-guarantees
type: qa
source: snowflake-docs
---
## Q
一个多线程的 Python 程序让所有线程共用一个 Snowflake 连接，结果线程 A 刚写入的数据被莫名其妙地回滚了。原因是什么？该怎么避免？

## A
Snowflake 的事务绑定在单个会话（session）上，多个会话不能共享一个事务；但共用同一连接的多个线程属于同一个会话，因此也共享同一个事务。线程 B 执行的 ROLLBACK（或修改 AUTOCOMMIT）会作用于所有线程，异步运行时结果不可预测。解决办法是每个线程使用独立连接，或让线程同步执行以控制步骤顺序；即便分开连接，不同事务之间仍可能有竞态。
