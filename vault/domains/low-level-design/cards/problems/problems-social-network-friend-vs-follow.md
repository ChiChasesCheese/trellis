---
id: problems-social-network-friend-vs-follow
node: problems.social.social-network
type: qa
step: 1
tags: [grown]
---
## Q
在社交网络（Social Network）设计里，为什么好友（friend）和关注（follow）要建成两套独立的关系，而不是用其中一种模拟另一种？

## A
两者回答不同的问题：好友是**信任圈**，靠请求—接受成对创建，双方地位对等，决定“仅好友可见”这一档隐私——只用关注模拟不出这种对称同意的语义。关注是**内容订阅**，单向、无需对方同意，决定信息流里能刷到谁——只用好友模拟不出“我想看一个不认识的公众人物的动态”这种不对称场景（大V账号的存在本身就要求单向关系）。两者不是互相替代，本设计让 `accept_friend_request` 顺带建立双向关注，把体验接起来，但 `unfriend` 不强制取关、`unfollow` 不影响好友关系，各自的代价被诚实保留。
