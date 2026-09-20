---
nodes: [problems.social.social-graph-search]
url: https://www.usenix.org/conference/atc13/technical-sessions/presentation/bronson
---
# TAO: Facebook's Distributed Data Store for the Social Graph

值得读：USENIX ATC 2013 论文，披露了 Facebook 真实图存储的对象/关联（object/
association）数据模型、按 id 分片、leader/follower 缓存分层、跨地域异步复制，以及
"十亿级读/秒、96.4% 整体缓存命中率、99.8% 请求是读"这些生产数字。本题解用它的缓存命中率
佐证"图查询重复率高、缓存不需要做得很精巧"，也用它披露的跨地域异步复制模式作为本设计
"边写入选择强一致"这一决定的对照组——本设计的写入量级远低于 TAO 服务的真实规模，所以能
负担得起 TAO 为了性能而放弃的强一致性。
