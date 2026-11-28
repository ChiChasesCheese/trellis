---
id: hi-c-sd-postgres-n05-jsonb
node: sd.deep-dives.postgres.notes
type: qa
step: 5
---
## Q
**PostgreSQL · JSONB 与 GIN：灵活的属性**｜摘要 · 必会

帖子有的带位置、有的带话题标签，字段各不相同，怎么在关系库里存？

## A
- **JSONB 列：** 把可变属性放进一个二进制 JSON 列，不必为每种可能的属性单独加列，随时可以加新属性，像 NoSQL 一样灵活。
- **查询要靠 GIN 索引：** 在 JSONB 列上建 GIN 索引后，`metadata @> '{"type": "video"}'` 这类"包含"查询可以走索引，而不是逐行解析。
- **组合：** 用 `@>` 可同时匹配多个键，如视频类型加某个话题标签，或者找出提到某个用户的帖子。
- **意义：** 结构化数据和半结构化数据放在同一个库里，事务一致，往往可以代替另一个文档数据库。
