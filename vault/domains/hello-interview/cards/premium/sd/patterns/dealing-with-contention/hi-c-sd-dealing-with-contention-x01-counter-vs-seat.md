---
id: hi-c-sd-dealing-with-contention-x01-counter-vs-seat
node: sd.patterns.dealing-with-contention.exam
type: qa
step: 1
---
## Q
**处理竞争 · 计数对了座位却重复**｜考点 · 必会

你的方案是 `UPDATE ... SET available_seats = available_seats - 1 WHERE available_seats > 0`，再插一条带座位号的订单。库存剩 20 张时压测发现同一座位被卖给两人，计数却完全准确。为什么，怎么改？

## A
- **原因：** 守卫保护的是计数器，而人们争的是具体座位。两次扣减都成功（20、19 都大于 0），两条订单写入同一个座位号。
- **改法：** 一座一行，对座位行做条件写：`SET status='sold' WHERE seat=? AND status='available'`，第二个匹配 0 行。

```mermaid
sequenceDiagram
    participant A as 事务 A
    participant DB as 数据库
    participant B as 事务 B
    A->>DB: 计数 20 > 0，扣减
    B->>DB: 计数 19 > 0，扣减
    A->>DB: 插订单，座位号 S
    B->>DB: 插订单，座位号 S
    Note over A,B: 守卫在计数器上，同一座位两张订单
    A->>DB: 座位行 SET sold WHERE status='available'
    DB-->>A: 1 行，售出
    B->>DB: 同样的条件写
    DB-->>B: 0 行，失败
```

- **补充：** 计数变成派生数据，同一事务内更新缓存的计数，或由座位行统计。
- **资深加分：** 一句话概括原则：守卫必须落在被争抢的那个资源上，数据库只能保护它看得见的冲突。
