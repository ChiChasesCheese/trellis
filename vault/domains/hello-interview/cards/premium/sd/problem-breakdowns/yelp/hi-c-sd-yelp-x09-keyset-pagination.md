---
id: hi-c-sd-yelp-x09-keyset-pagination
node: sd.problem-breakdowns.yelp.exam
type: qa
step: 9
---
## Q
**Yelp · 一个商户有 10 万条评价，评价翻页怎么做**｜考点 · 追问

评价接口是 `GET /businesses/:id/reviews?page=`，按时间倒序。用户翻到第 5000 页（每页 20 条）。用 `OFFSET` 会怎样？怎么改？

## A
- **OFFSET 的代价：** 第 5000 页要先跳过 4999 × 20 = 99980 行再取 20 行，数据库仍要顺着索引扫过这近 10 万行；页数越靠后越慢，扫描量与页码成正比。
- **并发插入的错位：** 翻页过程中有新评价插入，后面页的内容整体后移一格，用户会看到重复的条目。
- **键集分页（keyset pagination）：** 返回结果里带上最后一条的 `(created_at, id)` 作为游标，下一页用 `WHERE (created_at, id) < (:c, :i) ORDER BY created_at DESC, id DESC LIMIT 20`，走联合索引，每页成本相同，不受深度影响，也不受新插入影响。
- **代价：** 不能直接跳到第 N 页，只能顺序往后翻；评价列表通常本来就是顺序浏览。
- **要点：** 大数据集分页用游标，游标键要有唯一性（加上 id 打破并列）。
