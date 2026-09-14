---
id: tag-lineage-propagation
node: security.data-classification-and-tagging
type: qa
tags: [grown]
---
## Q
Snowflake 的对象标签（object tag）是什么类型的对象？标签在对象层级上怎样生效？

## A
标签是模式级对象，是一个键，可以以“键 = 字符串值”的形式附加到账户、仓库、数据库、模式、表、列等对象上。附加到父对象上的标签会被其子对象继承（如给模式打的标签作用于其中的表和列），子对象上直接设置的同名标签值会覆盖继承值。可以通过 ACCOUNT_USAGE 的 `TAG_REFERENCES` 视图等查询哪些对象带有某个标签，用于审计和成本归属等场景。
