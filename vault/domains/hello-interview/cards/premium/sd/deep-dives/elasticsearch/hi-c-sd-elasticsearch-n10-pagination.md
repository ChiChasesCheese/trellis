---
id: hi-c-sd-elasticsearch-n10-pagination
node: sd.deep-dives.elasticsearch.notes
type: qa
step: 10
---
## Q
**Elasticsearch · 分页：from/size、search_after、PIT 游标**｜摘要 · 必会

深分页为什么慢？`search_after` 怎么用？它的局限是什么？PIT 解决什么？

## A
- **`from` + `size`：** 最简单，指定起点和条数。深分页（超过约 1 万条）很低效，因为每次要取出并排序前面所有文档。
- **`search_after`：** 用上一页最后一条的排序值作为下一页的边界，Elasticsearch 只返回排在边界之后的命中，不用收集再跳过前面所有页。排序要带一个唯一的决胜字段（如 `_id`）。
- **它的局限：** 排序值只是书签，不是磁盘地址，每页仍要执行查询。两次请求之间文档增删改会使结果围绕书签移动，可能漏一条或重复一条；客户端要保存最后一条的排序值；只能向前翻。
- **游标（PIT + `search_after`）：** 先 `POST /index/_pit?keep_alive=1m` 得到 PIT ID，之后每次搜索带上 `pit`，第二页起加 `search_after`，结束时 `DELETE /_pit`。PIT 让整个翻页过程看到一致的数据快照，即使索引在更新；代价是有状态，开销更大。
