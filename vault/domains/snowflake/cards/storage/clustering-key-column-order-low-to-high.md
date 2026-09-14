---
id: clustering-key-column-order-low-to-high
node: storage.clustering-keys
type: qa
source: snowflake-docs
---
## Q
定义多列聚簇键 `CLUSTER BY (a, b)` 时，列的顺序该怎么排？排反了会怎样？

## A
一般按基数（cardinality，不同值数量）从低到高排列。如果把高基数列放在低基数列前面，数据会先按高基数列分散开，后面那一列几乎无法再聚到一起，对它的聚簇效果会明显变差。另外单个聚簇键建议最多 3–4 个列或表达式，再多通常成本增长快于收益。
