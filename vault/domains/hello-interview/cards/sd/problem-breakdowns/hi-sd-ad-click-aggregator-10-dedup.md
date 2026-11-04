---
id: hi-sd-ad-click-aggregator-10-dedup
node: sd.problem-breakdowns.ad-click-aggregator.exam
type: qa
step: 10
---
## Q
**点击幂等：展示 ID 与签名**｜系统设计 · 问题拆解

怎样保证同一次点击不被重复计数？为什么按 userId 加 adId 去重不对？展示 ID（impression ID）方案是什么，怎样防伪造？

## A
**要点。**
- 差：要求登录，按 userId + adId 去重。要求所有用户都登录不现实；而且再营销（retargeting）会故意多次向同一用户展示同一广告，应该是每次展示算一次点击，而不是每个用户每个广告一次。
- **好：服务端发 impression ID：** 好：广告投放服务为每次展示生成唯一的 impression ID，随广告发给浏览器，点击时带回。去重键就是它。

**取舍。** 去重要在进入流之前做，因为窗口边界两侧的重复点击在 Flink 里会被算两次。点击先查缓存，已存在就忽略；否则先写流，再把 ID 写缓存（先写流，缓存更新失败最多多一次重复，由对账修正，而丢点击无法恢复）。

**防伪造。** 恶意用户可伪造大量唯一 ID。用 HMAC 加密钥对 impression ID 与 adId 一起签名，点击时校验；HMAC 校验是微秒级，延迟可忽略。

**数字。** 每天 1 亿个唯一 ID × 16 字节 = 1.6 GB，用 Redis Cluster 加持久化（RDB 或 AOF）和副本即可。
