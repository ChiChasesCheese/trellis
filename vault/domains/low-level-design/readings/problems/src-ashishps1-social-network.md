---
nodes: [problems.social.social-network]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/social-networking-service.md
---
# awesome-low-level-design — Designing a Social Networking Service

值得读：题面覆盖好友请求、发帖、信息流、点赞评论、隐私可见范围与通知，五种语言各一份实现，
用来对齐"面试官脑子里的完整清单"最省事。它的 Python 版把一切塞进一个 `SocialNetworkingService`
单例，用 `ConcurrentHashMap`（对应 Python 里就是普通 `dict`）"隐式线程安全"，信息流现场遍历
好友的帖子再排序，没有区分推/拉两种代价、也没有大V这回事——所有好友一视同仁地全量扫描。本题解
把关系（`SocialGraph`）、内容（`ContentStore`）、信息流（`FeedService`）拆成三个不持有彼此
单例引用的类，并且显式讨论了写扩散在大V账号上会失效、必须换成读时合并，这是原实现完全没有
覆盖的问题。
