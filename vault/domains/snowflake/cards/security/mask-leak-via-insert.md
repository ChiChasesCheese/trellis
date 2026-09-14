---
id: mask-leak-via-insert
node: security.column-masking-policies
type: qa
source: snowflake-docs
---
## Q
源表的 ssn 列有脱敏策略（masking policy），一个能看到明文的角色执行 `INSERT INTO t2 SELECT ssn FROM t1`，而 t2 的列上没有策略。会有什么风险？

## A
脱敏只发生在查询时，不随数据流动。能看明文的角色插入的就是明文，而 t2 列没有策略，任何对 t2 有足够权限的角色都能直接看到敏感值，造成泄露。反过来，看到脱敏值的角色插入的值会保持脱敏状态，导致目标列里明文与脱敏值混杂。因此要识别源列数据可能流向的所有目标表并同样施加策略，发布前验证涉及受保护列的查询。
