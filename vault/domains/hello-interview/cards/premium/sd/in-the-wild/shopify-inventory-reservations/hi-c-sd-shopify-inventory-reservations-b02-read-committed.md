---
id: hi-c-sd-shopify-inventory-reservations-b02-read-committed
node: sd.in-the-wild.shopify-inventory-reservations.beyond
type: qa
step: 2
---
## Q
**Shopify 库存预留 · READ COMMITTED 的代价**｜拓展 · 加分

改用 READ COMMITTED 避免间隙锁，会带来什么新的风险？

## A
- **允许不可重复读和幻读：** 同一事务里两次查询可能看到别的事务已提交的新数据。依赖"两次读到的一样"的逻辑会出问题；预留事务本来就是"加锁后立刻修改"，对此不敏感。
- **复制要求：** MySQL 在 READ COMMITTED 下要求基于行的二进制日志（binlog_format 为 ROW）；用基于语句的复制会被拒绝或不安全。
- **取舍：** 隔离级别应按事务粒度选用，只给这类加锁扫描降级，其余事务保持默认。在代码库里第一次使用非默认级别，意味着要写清楚原因和约束。
- **面试用法：** 被追问死锁，讲"间隙锁来自可重复读，缩小事务和降低隔离级别是手段"。
