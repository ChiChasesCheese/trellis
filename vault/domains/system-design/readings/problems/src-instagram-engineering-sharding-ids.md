---
nodes: [problems.social.instagram]
url: https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c
---
# Sharding & IDs at Instagram

值得读：Instagram 早期工程团队披露的真实 64 位自增 ID 方案——41 位毫秒时间戳（自定义
从 2011 年起算的 epoch，而不是 Unix epoch）、13 位逻辑分片 id（预留 8,192 个分片，
早期只启用约 2,000 个）、10 位序列号（每个分片每毫秒最多生成 1,024 个 id），并解释了
为什么放弃 Twitter Snowflake（额外引入 ZooKeeper 等"活动部件"）和 ticket server（写入
瓶颈和运维负担）这两个备选方案，选择用 PostgreSQL 的 schema 特性把逻辑分片映射到物理
数据库。本题解在引用这组数字时，自己重新算了一遍 41 位毫秒时间戳的可寻址跨度：精确计算
约为 69.7 年，而不是常见转述里粗略给出的"41 年"——这是"数字必须自己算，不能照抄"这条
规则的一个具体例子，也是本题解和很多转述这篇文章的二手资料的分歧所在。
