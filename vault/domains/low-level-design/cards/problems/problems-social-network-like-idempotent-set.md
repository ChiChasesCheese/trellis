---
id: problems-social-network-like-idempotent-set
node: problems.social.social-network
type: qa
step: 7
tags: [grown]
---
## Q
社交网络里点赞用 `dict[post_id, int]` 计数器（点一次 `+1`）会有什么真实的 bug？应该怎么设计存储？

## A
同一个用户重复点击、客户端超时重试、或者双击误触，都会让计数器变成 2、3……而产品语义应该是“仍然是赞过的状态”，点赞数因此被错误地抬高。正确的存储是 `dict[post_id, set[user_id]]`：`like()` 检查用户是否已在集合里，不在才加入并返回 `True`，已经在则返回 `False`（幂等，无副作用）；`like_count` 就是集合的大小，天然去重；`unlike` 直接从集合里删除。多付出的代价是每个赞存一个用户 id 而不是一个整数，在社交网络的规模下不是问题；换来的是“点一次”和“点很多次”永远得到同一个结果。
