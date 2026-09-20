---
id: problems-social-network-comment-independent-entity
node: problems.social.social-network
type: qa
step: 8
tags: [grown]
---
## Q
社交网络的机考第 4 关要求加评论和点赞功能，判分点是什么？这两个功能应该怎么加才能满足它？

## A
判分点是：加评论和点赞**不需要改动信息流生成的任何一行代码**（`FeedService.publish` 和 `get_feed` 都不动）。做法是把评论建成独立实体 `Comment`（自己的 id、作者、时间，引用 `post_id` 而不是被塞进 `Post` 的一个列表字段），评论数从评论字典的长度派生而不是单独维护一个计数字段；点赞是一个 `post_id -> set[user_id]` 的映射，与帖子对象本身解耦。两者都只依附在 `ContentStore` 一侧，`FeedService` 从不需要知道某条帖子有没有评论或点赞——信息流只关心“这条帖子对这个人是否可见”，与它下面挂了多少互动无关，这正是把内容存储和信息流拆成两个不同类、互不持有引用的价值所在。
