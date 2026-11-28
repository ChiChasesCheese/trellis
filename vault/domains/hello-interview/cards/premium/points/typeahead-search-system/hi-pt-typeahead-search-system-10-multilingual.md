---
id: hi-pt-typeahead-search-system-10-multilingual
node: qb.sd.typeahead-search-system.points
type: qa
step: 10
---
## Q
**搜索联想 · 多语言与地区**｜追问 · 出自：搜索联想 › 深入 6

联想要支持多种语言和地区，快照和键怎么设计？

## A
**做法。** 快照按语言和地区分别构建，`lang`、`region` 作为键的一部分。

**注意。** 分词语言（中文、日文）用分词后的词首或字符前缀，要先问清；不同语言热度分布不同，不能混在同一张表里排序。
