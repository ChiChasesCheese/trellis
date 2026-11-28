---
id: hi-c-sd-google-news-n05-offset-pagination
node: sd.problem-breakdowns.google-news.notes
type: qa
step: 5
---
## Q
**新闻聚合 · 基础版无限滚动：基于页码**｜摘要 · 必会

最朴素的无限滚动怎么实现？它在什么条件下会出问题？

## A
- **做法：** 客户端发 `GET /feed?region=US&limit=20&page=1`，动态流服务查地区内最近 20 篇（按发布时间排序），响应带分页信息（总页数、当前页）；用户接近底部时自动请求下一页，服务端算出偏移 `(page-1) × limit`，用 `OFFSET … LIMIT …` 取数据，如此反复。
- **优点：** 实现简单，是个能工作的起点。
- **局限：** 有性能和一致性问题：OFFSET 越大数据库越要先跳过更多行；新文章不断加入时，内容整体下移，翻页会重复或漏掉文章。这正是第一个深入问题。
