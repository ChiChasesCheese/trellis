---
id: distributed-multi-leader-retrofit-hazards
node: distributed.replication.multi-leader
type: qa
---
## Q
You turn on multi-leader replication between two datacenters of a database designed for a single leader. Beyond same-key write conflicts, which database features quietly break, and why?

## A
Features that assumed "exactly one node assigns/enforces this" now run independently on every leader:

- **Auto-increment keys collide**: both leaders hand out id 42. Workaround: interleave ranges (one leader issues odd, the other even) or switch to UUIDs/snowflake ids.
- **Uniqueness and other global constraints can't be enforced**: each leader can only check its own local state at write time, so two "unique" usernames can both commit and only conflict later, when the invariant is already violated.
- **Triggers, stored procedures, and side-effectful writes** may fire once per leader when the replicated write is applied — duplicate emails, double-counted counters — unless replication apply is explicitly excluded.

Interview point: this is why bolt-on multi-master modes of classic RDBMSs are treated as a last resort — the *data* replicates, but the single-writer assumptions baked into the features do not.

## Q zh
你在一个为单 leader 设计的数据库上，为两个数据中心开启了多主复制（multi-leader）。除了同一 key 的写冲突之外，哪些数据库特性会悄悄失效？为什么？

## A zh
那些默认"只有一个节点负责分配/校验"的特性，现在会在每个 leader 上各自独立运行：

- **自增主键冲突**：两个 leader 都发出 id 42。变通：错开号段（一个发奇数、一个发偶数），或改用 UUID/snowflake id。
- **唯一性等全局约束无法强制**：每个 leader 写入时只能检查自己本地的状态，于是两个"唯一"的用户名都能提交成功，冲突要到之后同步时才暴露，而那时不变量已经被破坏。
- **触发器、存储过程和带副作用的写入**在应用复制过来的写时可能在每个 leader 上各触发一次——邮件发两遍、计数器翻倍——除非显式地让复制应用路径绕过它们。

面试要点：这正是经典关系库"外挂式" multi-master 模式被当作最后手段的原因——*数据*复制过去了，但那些特性里内建的单写者假设并不会跟着复制。
