---
id: hi-pt-web-crawler-restricted-communication-2-ownership
node: qb.sd.web-crawler-restricted-communication.points
type: qa
step: 2
---
## Q
**无中心网络爬虫 · 哈希所有权去重**｜必会 · 出自：无中心网络爬虫 › 深入 1

没有任何中心组件时，怎样保证 10,000 个节点之间同一个 URL 不会被下载两次？

## A
**选择。** 对规范化的完整 URL 哈希，每个 URL 有唯一的主人节点（一致性哈希，带虚拟节点）；"检查并插入已见集合"只在主人一处发生，是单一写者，不需要分布式锁或共识。

**前提。** 成员表是静态配置的（约 200 KB），所有节点对"谁是主人"的答案一致。

**易错。** 规范化不一致，会让同一页面有两个主人。
