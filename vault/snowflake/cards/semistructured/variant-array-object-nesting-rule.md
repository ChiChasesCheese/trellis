---
id: variant-array-object-nesting-rule
node: semistructured.variant-type-storage
type: cloze
source: snowflake-docs
---
Snowflake 半结构化类型的嵌套规则：{{c1::VARIANT}} 可以容纳任意其他类型的值（包括 ARRAY 和 OBJECT）；而 ARRAY 的每个元素和 OBJECT 每个键值对中的值，类型都是 {{c2::VARIANT}}。正是这种互相包含，才能搭出任意深度的层级结构。
