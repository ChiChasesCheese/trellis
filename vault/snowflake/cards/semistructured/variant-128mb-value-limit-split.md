---
id: variant-128mb-value-limit-split
node: semistructured.variant-type-storage
type: qa
source: snowflake-docs
---
## Q
某个 JSON 文档中单个值需要大约 128 MB 以上的存储空间，整份放进一个 VARIANT 列会有问题。有什么建模办法？

## A
当数据很复杂或单个值需要超过约 128 MB 的存储时，应组合使用多种存储方式：把数据拆分到多个列中（可以用显式的抽取转换，也可以自动检测列定义），其中部分列仍可保存显式指定的 VARIANT/ARRAY/OBJECT 层级，从而让每个值都控制在单值上限之内。
