---
id: hi-c-lld-patterns-n04-builder
node: lld.in-a-hurry.patterns.notes
type: qa
step: 4
---
## Q
**设计模式 · Builder：分步构造复杂对象**｜摘要 · 必会

Builder 什么时候用？为什么多数 LLD 题不需要？

## A
- **用处：** 对象有许多可选部分或配置项，避免十个参数一半为空的构造函数
- **常见出现：** HTTP 请求、数据库查询、配置对象、API 客户端
- **做法：** 链式设置，最后 `build()` 校验必填项
- **不必用：** 题目没描述复杂对象时；多数领域对象只有二到四个必填字段，普通构造函数就够
- **Python：** 有默认值的数据类、关键字参数通常更好
