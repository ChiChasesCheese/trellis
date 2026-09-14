---
id: ddl-inside-nested-procedure-error
node: txn.ddl-as-transaction
type: qa
source: snowflake-docs
---
## Q
外层存储过程开启了事务，然后调用内层存储过程，内层执行了一条 `DROP TAG`。为什么这会直接报错？

## A
大多数 DDL 会隐式提交当前活跃事务，而这个事务是在另一个作用域（外层存储过程）中开启的；Snowflake 不允许一个作用域提交另一个作用域开启的事务，所以该命令返回错误。规避办法是：可能在他人开启的事务中被调用的存储过程里，不要执行 DDL 或其他会隐式提交的命令。
