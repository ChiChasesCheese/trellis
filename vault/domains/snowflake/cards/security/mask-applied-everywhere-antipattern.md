---
id: mask-applied-everywhere-antipattern
node: security.column-masking-policies
type: qa
source: snowflake-docs
---
## Q
email 列挂了脱敏策略（masking policy），无权限用户执行 `WHERE email = 'alice@x.com'` 却查不到任何行，即使该行存在。为什么？

## A
脱敏策略会被施加到该列在 SQL 中被引用的每一处——投影、JOIN 谓词、WHERE 谓词、ORDER BY/GROUP BY——目的是防止用户通过巧妙构造查询（比如用 WHERE 逐个猜值）来反推被脱敏的原值。因此 WHERE 中的 email 先被替换成脱敏后的值，再与明文常量比较，只脱敏了比较的一侧，自然匹配不上。这是常见的反模式（anti-pattern），JOIN 谓词中使用受保护列也有同样的问题。
