---
id: hi-c-sd-dealing-with-contention-x02-zero-rows-trap
node: sd.patterns.dealing-with-contention.exam
type: qa
step: 2
---
## Q
**处理竞争 · 受影响行数为零**｜考点 · 必会

同事写了事务：先条件 `UPDATE` 扣库存，再无条件 `INSERT` 订单，说"扣不到库存会报错回滚，所以安全"。指出问题并给出两种修法。

## A
- **问题：** `UPDATE` 匹配 0 行不是错误，语句成功，事务不会回滚，后面的 `INSERT` 照常执行，没抢到座位的人得到一张订单。
- **修法一：** 在 SQL 里把插入依赖更新的结果（`WITH r AS (UPDATE ... RETURNING ...) INSERT ... SELECT ... FROM r`），没改到行就插入 0 条。
- **修法二：** 应用里读受影响行数，为 0 就回滚。

```mermaid
flowchart TB
    U["条件 UPDATE 扣库存"] --> Z{"匹配行数"}
    Z -->|"1"| I1["INSERT 订单：正确"]
    Z -->|"0：不报错、不回滚"| I2["INSERT 照常执行<br/>没抢到的人也拿到订单"]
    I2 -.->|"修法一"| F1["WITH r AS (UPDATE … RETURNING …)<br/>INSERT … SELECT … FROM r → 插入 0 条"]
    I2 -.->|"修法二"| F2["读受影响行数，为 0 就回滚"]
```

- **同样的陷阱出现在：** 乐观并发的版本检查（版本过期同样是 0 行，不报错）。
