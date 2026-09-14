---
id: networking-cursor-vs-offset-pagination
node: networking.api-styles
type: qa
---
## Q
Offset vs cursor pagination in an API — what breaks with `OFFSET` at depth and under concurrent writes?

## A
- **Cost**: `OFFSET n` scans and discards n rows — page 10,000 does O(n) work; deep pagination becomes a DB DoS.
- **Instability**: rows inserted/deleted between page fetches shift every offset → items duplicated or skipped mid-scroll.

**Cursor (keyset)**: return an opaque token encoding the last seen sort key; next page is `WHERE (created_at, id) < (cursor) ORDER BY created_at, id LIMIT k` — index seek, O(log n), stable under writes.

Price: no "jump to page N", and the sort key must be unique and immutable (hence the id tiebreaker).

## Q zh
API 中的偏移与游标分页 — `OFFSET` 在深度和并发写入下会破坏什么？

## A zh
- **成本**：`OFFSET n` 扫描并丢弃 n 行 — 第 10,000 页执行 O(n) 工作；深分页成为数据库 DoS。
- **不稳定性**：在页面获取之间插入/删除的行转移每个偏移 → 项目在滚动中重复或被跳过。

**游标（keyset）**：返回编码最后看到的排序键的不透明令牌；下一页是 `WHERE (created_at, id) < (cursor) ORDER BY created_at, id LIMIT k` — 索引查找，O(log n)，在写入下稳定。

价格：没有"跳到第 N 页"，排序键必须是唯一且不可变的（因此需要 id 系结器）。
