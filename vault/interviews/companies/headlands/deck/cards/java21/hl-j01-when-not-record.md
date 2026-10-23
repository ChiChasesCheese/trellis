---
id: hl-j01-when-not-record
node: java21.j01-record
type: qa
step: 28
---
## Q
哪五种场景不适合用 `record`？各自该用什么？

## A
1. **需要可变状态**（计数器、累加器）：用普通类。
2. **需要继承层次**：`record` 不能 `extends`；但可以 `implements` 一个 `sealed interface`，这是最常见的搭档。
3. **框架要求无参构造器 + setter**（经典 JPA 实体、部分老序列化框架）：`record` 不满足。
4. **组件特别多**（十几个）：构造时参数顺序容易错，考虑构建器（builder）模式。
5. **公共 API**：给 `record` **增加组件**会改变构造器签名，二进制不兼容，发布前要想清楚。
