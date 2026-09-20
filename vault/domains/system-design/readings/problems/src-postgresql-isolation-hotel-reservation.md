---
nodes: [problems.commerce.hotel-reservation]
url: https://www.postgresql.org/docs/current/transaction-iso.html
---
# Transaction Isolation

值得读：官方文档精确描述了读已提交隔离级别下，`UPDATE` 命令在目标行被并发未提交事务修改
时的行为——等待第一个事务提交或回滚，然后针对更新后的行版本重新求值自己的 `WHERE` 子句。
本题据此论证了"单条多行条件更新"为什么在读已提交下就足够安全，而不需要笼统地说"用事务"；
比大多数题解文章更细的地方是明确了"UPDATE 只更新匹配行、不会让整条语句因部分行不匹配而失
败"这一 SQL 语义，进而在文中补上了应用层检查受影响行数这一步。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.postgresql.org/docs/current/transaction-iso.html)

## Archived copy
![[src-postgresql-isolation-hotel-reservation-clip]]
%% trellis:end %%
