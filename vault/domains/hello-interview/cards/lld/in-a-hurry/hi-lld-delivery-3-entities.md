---
id: hi-lld-delivery-3-entities
node: qb.lld.beverage-vending-system.pre-lld-in-a-hurry-delivery
type: qa
step: 3
---
## Q
**第二步：从需求里找实体和关系**｜低层设计 · 速览

怎么从需求里挑出核心实体，怎么定义它们之间的关系？白板上需要画到什么程度？

## A
**找实体。** 扫描需求，抽出有意义的名词。过滤标准：如果某个东西有会变化的状态，或者要执行规则，它大概就该是一个独立实体；如果只是附着在别的东西上的信息，它多半只是另一个类的字段。这样可避免拆出太多微型对象。

**定关系。** 想清楚：
- 谁是协调者（orchestrator），驱动主流程
- 谁拥有需要持久的状态
- **实体间如何依赖：** 它们如何依赖（has-a、uses、contains）
- 具体规则应当放在哪

**画法。** 一个实体清单加几个箭头表示谁拥有或使用谁，就足够了，不需要完整的 UML。重点是沟通清楚，而不是符号规范。

**例子（井字棋）。** 实体：Game、Board、Player。关系：Game 持有一个 Board，Game 持有两个 Player。Game 是协调者。
