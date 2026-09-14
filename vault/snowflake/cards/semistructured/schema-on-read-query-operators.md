---
id: schema-on-read-query-operators
node: semistructured.schema-on-read-parsing
type: cloze
source: snowflake-docs
---
在 Snowflake 中查询 VARIANT 等半结构化列时，内置运算符支持三类取值：按{{c1::下标访问 ARRAY 中的元素}}、按{{c2::键从 OBJECT 中取出对应的值}}、以及{{c3::沿路径逐层遍历 VARIANT 中的层级}}；XML 数据则用 {{c4::`XMLGET`}} 函数按标签取值。
