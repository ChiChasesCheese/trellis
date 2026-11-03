---
id: hi-pt-web-crawler-design-6-robots-rate
node: qb.sd.web-crawler-design.points
type: qa
step: 5
---
## Q
**网络爬虫 · robots.txt 与限速实现**｜必会 · 出自：网络爬虫 › 深入 1

robots.txt 和 Crawl-delay 怎么处理？限速是用 Redis 锁还是别的办法？节点宕机会怎样？

## A
**robots。** 每主机首次访问前拉取解析，缓存一天左右；`Disallow` 路径直接丢弃；Crawl-delay 换算成主机下次允许时间。
**限速。** 简单做法是 Redis `SET NX` 加同等 TTL 作主机锁；更好的是按主机哈希固定归属，状态本地化，省掉网络往返和锁竞争。
**宕机。** 哈希环重新分配，礼貌计时从零开始，最多一次略快的访问，可接受。给等待时间加随机抖动避免共振。
