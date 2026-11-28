---
id: hi-c-sd-instagram-n06-feed-basic
node: sd.problem-breakdowns.instagram.notes
type: qa
step: 6
---
## Q
**Instagram 图片分享 · 最简动态流与索引**｜摘要 · 必会

最朴素的动态流怎么实现？需要什么索引，为什么选 DynamoDB？

## A
- **读时扇出（fan-out on read）：** 查我关注的所有人 → 对每个人查最近的帖子 → 合并后按时间排序 → 带游标截取返回。每一步都是读请求时现算。
- **没有索引就是全表扫描：** 每个用户都扫全部 Follow 行、再扫全部帖子，不可用。
- **索引设计（DynamoDB）：**
  - Follow：分区键 followerId，排序键 followedId，"我关注了谁"一次查询；
  - Post：分区键 userId，排序键 createdAt + postId，某人的帖子按时间有序，并且 postId 保证唯一。
- **为什么选它：** 关系简单、规模大、最终一致就够，所以水平扩展强的 NoSQL 合适；换成 PostgreSQL 也完全可以，只要说得出理由（现实中 Instagram 的主元数据库就是 PostgreSQL，说明关系库能扛这个量）。
- **隐患：** 如果我关注了几千人，这个流程极慢，这正是后面深入问题要解决的。
