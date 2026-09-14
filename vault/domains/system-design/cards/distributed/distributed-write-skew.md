---
id: distributed-write-skew
node: distributed.transactions.isolation
type: qa
---
## Q
On-call rule: at least one doctor must stay on shift. Two doctors, in concurrent transactions, each check "≥2 on call" and sign themselves off. Both commit under snapshot isolation. Name the anomaly and two fixes.

## A
**Write skew**: each transaction's read set was invalidated by the *other's* write, but since they wrote **different rows**, SI's write-write conflict detection sees nothing.

- **Serializable isolation** (e.g. Postgres SSI): tracks read-write dependencies and aborts one transaction — then retry.
- **Materialize the conflict / lock the invariant**: `SELECT ... FOR UPDATE` on the rows read (or a single row representing the shift), forcing the transactions to serialize on a common lock.

Pattern to recognize: *read a predicate, write based on it* — always suspect write skew under SI.

## Q zh
值班规则：至少要有一名医生留守。两名医生在各自的并发事务里，都检查了"在岗 ≥2 人"，然后都把自己签退了。两个事务在快照隔离下都提交成功。说出这个异常的名字，以及两种修复方式。

## A zh
**写倾斜（write skew）**：每个事务的读集都被**对方的写**打破了前提，但因为它们写的是**不同的行**，SI 的写写冲突检测什么都看不到。

- **可序列化隔离**（例如 Postgres 的 SSI）：跟踪读写依赖关系，中止其中一个事务——然后重试。
- **把冲突物化 / 给不变量加锁**：对读到的行（或一行代表这个班次的记录）执行 `SELECT ... FOR UPDATE`，强迫两个事务在一把共同的锁上串行化。

要学会识别的模式：*按谓词读，再基于它写*——在 SI 下永远要怀疑是不是写倾斜。
