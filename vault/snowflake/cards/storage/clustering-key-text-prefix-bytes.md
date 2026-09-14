---
id: clustering-key-text-prefix-bytes
node: storage.clustering-keys
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 中用 URL 这种前缀几乎都相同（如都以 `https://www.` 开头）的文本列做聚簇键（clustering key），为什么几乎没有效果？怎么改？

## A
文本聚簇键的元数据只跟踪每列的前几个字节：Clustering Classic 版本每列只用前 5 个字节（多字节字符集下可能不到 5 个字符），Optima Clustering 则所有键列合计最多用 1 KB。若前 N 个字符对每行都一样，这几个字节就没有区分度，聚簇等于无效。应改为对跳过相同前缀之后、基数合适的子串（substring）表达式做聚簇。
