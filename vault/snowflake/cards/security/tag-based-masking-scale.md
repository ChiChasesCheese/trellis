---
id: tag-based-masking-scale
node: security.data-classification-and-tagging
type: qa
tags: [grown]
---
## Q
一个账户里有上千个存放邮箱、手机号的列，分散在几十个库里，而且每周都有新表。逐列 `ALTER COLUMN ... SET MASKING POLICY` 为什么难以维持？基于标签的脱敏（tag-based masking）怎么解决？

## A
逐列挂策略需要知道每一个敏感列在哪，新表一建就可能漏挂，治理覆盖率随时间下降。基于标签的脱敏把脱敏策略（masking policy）挂到一个对象标签（tag，如 `pii_type`）上，而不是挂到具体列上：任何被打上该标签的列都会自动受对应策略保护。标签还可以打在表、模式或数据库上，由下层列继承，因此只要标签打对，新增的同类列自动被保护，治理从“管理几千个列”变成“管理几个标签”。
