---
id: hi-c-lld-introduction-x01-wrong-altitude
node: lld.in-a-hurry.introduction.exam
type: qa
step: 4
---
## Q
**LLD 导论 · 层次跑偏**｜考点 · 必会

LLD 轮次的题目是"设计一个网约车后端"，你却发现自己在讲 Kafka 分区和数据库分片。哪里错了，怎么拉回来？

## A
- **错在层次：** 这一轮要的是代码结构，不是服务拓扑；扩容和分片是系统设计的主题
- **拉回来：** 圈定一个核心流程（行程生命周期），列出实体（`Trip`、`Driver`、`Rider`、`TripState`）
- **然后：** 谈每个类持有什么状态、暴露什么方法、状态怎么转换
- **一句确认：** 开头问一句"这一轮聚焦单机内的对象设计，对吗"，能避免跑偏
