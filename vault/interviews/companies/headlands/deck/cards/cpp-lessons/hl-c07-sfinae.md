---
id: hl-c07-sfinae
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 12
---
## Q
面试问：什么是 SFINAE？现代 C++ 怎么写？
Interview question: What is SFINAE?

## A
- **SFINAE**（Substitution Failure Is Not An Error，替换失败不是错误）：重载解析时，某个模板实参替换出错，就**悄悄丢弃该候选**，不报错。
- 老写法靠它实现"对某类类型启用某个重载"，代码复杂、报错难读。
- **现代写法**：用 `if constexpr`（函数体内按类型分支）和 **concepts**（约束重载/模板）。
