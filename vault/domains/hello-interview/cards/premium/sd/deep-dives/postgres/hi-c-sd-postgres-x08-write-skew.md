---
id: hi-c-sd-postgres-x08-write-skew
node: sd.deep-dives.postgres.exam
type: qa
step: 10
---
## Q
**PostgreSQL · Repeatable Read 够用吗：写偏斜**｜考点 · 追问

医院规定至少 1 名医生值班。两位医生同时执行：先查值班人数是否大于 1，是就把自己设为下班。在 Repeatable Read 下可能出什么问题？怎样修复？

## A
- **问题（写偏斜，write skew）：** 两人各自在自己的快照里看到有 2 人值班，都通过检查，各改自己的那一行，提交后值班人数是 0。两个事务改的是不同的行，没有行冲突，所以快照隔离发现不了。
- **说明：** PostgreSQL 的 Repeatable Read 防住了幻读，但"序列化异常"仍可能出现。

```mermaid
sequenceDiagram
    participant A as 医生 A 的事务
    participant DB as 数据库（Repeatable Read）
    participant B as 医生 B 的事务
    A->>DB: 查值班人数
    DB-->>A: 2（A 的快照）
    B->>DB: 查值班人数
    DB-->>B: 2（B 的快照）
    A->>DB: 改 A 那一行为下班，提交
    B->>DB: 改 B 那一行为下班，提交
    Note over A,B: 改的是不同行，没有冲突，值班人数 = 0
```

- **修法一：** 用 SERIALIZABLE，数据库检测到读写依赖形成环就回滚其中一个，应用重试。
- **修法二：** 在检查时对所有值班医生的行加 `FOR UPDATE`，让两个事务互相等待。
- **启示：** 当不变量涉及多行时，单行锁与快照都不够，要把相关的行都锁住或用 SERIALIZABLE。
