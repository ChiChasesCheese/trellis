---
id: hi-c-sd-google-news-n08-cursor-composite
node: sd.problem-breakdowns.google-news.notes
type: qa
step: 8
---
## Q
**新闻聚合 · 复合游标与单调递增 ID**｜摘要 · 必会

怎么让游标在时间戳重复时仍然精确？有没有更简单的办法？

## A
- **复合游标：** 游标 = 时间戳 + 文章 ID，如 `2024-01-15T10:30:00Z_article123`，构成唯一的全序，ID 当平局裁决。查询用元组比较：`WHERE (published_at, article_id) < (游标时间, 游标 ID) ORDER BY published_at DESC, article_id DESC LIMIT 20`，配 (published_at, article_id) 复合索引。不重复不漏；游标分页是时间线接口的通行做法（如 Twitter 的 `max_id` 按 ID 翻页，Graph API 用 `after` 游标）。代价：游标生成与解析稍复杂，查询稍复杂，索引多占一点空间，但完全值得。
- **单调递增 ID：** 更简单：让文章 ID 本身随时间递增（ULID 这类可按字典序排序的 ID，或数据库自增），游标就只是一个 ID，查询 `WHERE article_id < 游标 ORDER BY article_id DESC LIMIT 20`；只需 ID 上一个索引，也没有时间戳冲突。
- **代价：** 要在一开始规划 ID 策略，已用随机 UUID 的要迁移；分布式环境要协调 ID 生成，保持顺序。
- **结论：** 对按时间排序的数据，单调 ID 往往最简单最快；但要小心"ID 顺序"与"发布时间顺序"是否一致，见考点卡。
