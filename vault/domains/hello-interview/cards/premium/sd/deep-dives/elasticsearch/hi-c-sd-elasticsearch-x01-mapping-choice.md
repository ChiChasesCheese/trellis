---
id: hi-c-sd-elasticsearch-x01-mapping-choice
node: sd.deep-dives.elasticsearch.exam
type: qa
step: 1
---
## Q
**Elasticsearch · 给商品索引设计映射**｜考点 · 必会

商品文档：`sku`（唯一编号）、`name`（可全文搜索）、`brand`（按品牌过滤和统计）、`price`、`description`（长文本，不参与搜索，只展示）、`reviews`（数组，要查"同一条评论里评分≥4 且包含 battery"）。写出每个字段的类型，并说明为什么不是全部默认映射。

## A
- **`sku`：** `keyword`，整体精确匹配。**`name`：** `text`，分词后做全文匹配（需要按名称精确排序或聚合时再加一个 `keyword` 子字段）。**`brand`：** `keyword`，用于过滤和聚合。**`price`：** `float`（或用整数分，避免浮点误差）。
- **`description`：** 不参与搜索，就不要建索引（不让它进倒排索引），完整内容仍保存在 `_source` 里供展示，省下内存与索引体积。
- **`reviews`：** 声明为 `nested`。如果拍平成普通对象数组，评分和评论文本会被分别索引，"评分≥4 且包含 battery" 可能匹配到 A 评论评分高、B 评论含 battery 的错误组合。
- **为什么不全部默认：** 动态映射会为所有字段建索引，增加内存和体积；同时字段类型由首次出现的数据猜出来，可能与你期望不符。
- **评论更新频繁时：** 不要嵌套，改用单独的评论索引，查询时分两步，类似规范化。
