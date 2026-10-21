---
id: amz-in-memory-db-how-it-is-asked
node: amazon.amz-in-memory-db
type: qa
step: 1
tags: [grown]
---
## Q
内存数据库（In-Memory Database）要你设计什么？开场先问哪三个澄清问题？

## A
要写一个迷你数据库：先是按行号存取（插入自增、删除后行号不回退、读一个格子），再加列类型、WHERE、ORDER BY，再加 JOIN，最后解析 SQL 文本。

三个问题：
1. 列有类型吗？不符是报错还是转换？决定要不要在写入时检查类型。
2. 条件里遇到 NULL 怎么算？`age <> 2` 选 NULL 行吗？决定谓词是两值还是三值。
3. JOIN 只要等值吗，规模多大？只要等值才能用哈希连接。
