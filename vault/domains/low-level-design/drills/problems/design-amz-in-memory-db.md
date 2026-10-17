---
nodes: [amazon.amz-in-memory-db, structure.storage, patterns.structural]
tags: [problem]
---
# Drill：内存数据库（In-Memory Database）

在内存里写一个迷你数据库：能建表、增删改查、按条件筛选和排序、连接两张表，最后能执行 SQL 文本。规模是几张表、每张几百到几千行；先不考虑磁盘和并发。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 15 分钟）：按行号存取。`SQL(names, columns)`、`insert_row(name, row)` 在表尾追加并自增行号、`delete_row(name, row_id)` 删除（之后插入的行号不回退）、`select_cell(name, row_id, column_id)` 读一格。先回答：行号从哪里来，为什么不能是「当前行数 + 1」？
- 第 2 关（约 20 分钟）：列有类型的表与增删改查，再加 WHERE 与 ORDER BY。类型不符、主键重复、未知列都抛异常且不留半成品；更新要么全改要么不改；条件支持比较、`IN`、`IS NULL`、`AND` / `OR` / `NOT`，遵守三值逻辑；排序支持多个键、升降序混合、NULL 最小。
- 第 3 关（约 15 分钟）：JOIN。先写嵌套循环，再改成哈希连接；内连接与左连接；重名列必须用「别名.列名」限定。说出 NULL 键为什么不匹配。
- 第 4 关（选做）：SQL 文本前端：分词器加递归下降解析器，支持 CREATE / INSERT / SELECT / UPDATE / DELETE，`NOT` > `AND` > `OR`。再口头回答：怎么加索引、事务、线程安全？

**怎么练**：把 `vault/domains/low-level-design/problems/amz-in-memory-db/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-in-memory-db -q`。

**评分点**
- 说得出内存数据库要设计什么，并先问出列类型、NULL 语义、JOIN 范围三个澄清问题（[[amz-in-memory-db-how-it-is-asked]]）。
- 对象拆分清楚：表、谓词、连接描述、数据库、解析器各管一件事（[[amz-in-memory-db-objects-and-jobs]]）。
- 自增主键用只增不减的计数器，行存成 `{主键: 行}`（[[amz-in-memory-db-stage1-insert-with-autoincrement]]）。
- WHERE 用三值逻辑，只留结果为真的行，能举出 `<>` 与 `NOT IN` 的反例（[[amz-in-memory-db-null-three-valued-logic]]）。
- JOIN 用哈希连接，说得出构建与探测的复杂度、NULL 键与左连接的处理（[[amz-in-memory-db-hash-join]]）。
- 写操作先校验后动手，失败不留半成品（[[amz-in-memory-db-failure-update-is-atomic]]）。
- 解析器靠方法调用层次表达优先级，新增文本前端不改存储（[[amz-in-memory-db-followup-sql-text-parser]]）；能口述索引的维护与查询顺序（[[amz-in-memory-db-index-maintenance]]、[[amz-in-memory-db-limit-before-order-mistake]]）。

**题解**：[[solution-amz-in-memory-db]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
