---
id: hi-pt-url-shortener-design-5-hash-collision
node: points.url-shortener-design
type: qa
step: 5
---
## Q
**短链接服务 · 哈希方案的碰撞**｜出自：短链接服务 › 深入 1

用哈希生成短码：规范化 URL 后用 SHA-256 或 MurmurHash 取前 7 位转 base62。库里已有 10 亿条时碰撞概率有多大？怎么处理？

## A
**数字。** 空间约 3.5 万亿，新记录撞上已有短码的概率约 10 亿/3.5 万亿，约 0.03%，约 3500 次创建一次。
**要点。** 必须依赖数据库唯一约束，冲突时加盐重算。
**取舍。** 无状态、同一 URL 得同一短码，但写路径多了读后写。
