---
id: hi-c-lld-introduction-n02-vs-system-design
node: lld.in-a-hurry.introduction.notes
type: qa
step: 2
---
## Q
**LLD 导论 · LLD 和系统设计的区别**｜摘要 · 必会

LLD 面试和系统设计面试，在讨论对象和产出物上差在哪？

## A
- **系统设计：** 讲架构和规模（流量、存储、一致性、缓存、分片），白板上画方框和箭头，几乎不写代码
- **LLD（也叫 OOD，面向对象设计）：** 讲单个功能或服务的内部，产出类、方法、数据模型和状态转换，用（伪）代码表达
- **同一个网约车题目：** 系统设计画匹配、计价、位置三个服务加队列和数据库；LLD 只设计 `Trip`、`TripState`、`PricingCalculator` 如何协作，例如 `assign_driver` 只允许在 REQUESTED 状态下调用，否则抛错
- **一句话：** 系统设计是地图，LLD 是地图上某一栋楼的施工图
