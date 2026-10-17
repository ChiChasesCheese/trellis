---
id: amz-in-memory-db-failure-update-is-atomic
node: amazon.amz-in-memory-db
type: qa
step: 7
tags: [grown]
---
## Q
在内存数据库里，`UPDATE users SET id = 50 WHERE city = 'sf'` 命中两行会发生什么？怎么保证失败时表不变？

## A
两行都被改成主键 50，主键重复，必须整条语句失败。如果边改边检查，第一行已经改了，表停在一半。

做法：先收集命中的行，在副本上算出所有新行，校验类型，并检查新主键之间不重复、也不与不在本次修改里的旧键冲突；全部通过后才删旧行、写新行。冲突时抛 `ConstraintError`，表里一行都没变。`insert` 同理，检查都在写入字典之前。
