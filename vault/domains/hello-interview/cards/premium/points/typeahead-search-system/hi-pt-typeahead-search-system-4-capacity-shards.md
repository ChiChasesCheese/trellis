---
id: hi-pt-typeahead-search-system-4-capacity-shards
node: qb.sd.typeahead-search-system.points
type: qa
step: 4
---
## Q
**搜索联想 · 分片与版本切换的内存**｜必会 · 出自：搜索联想 › 深入 1

前缀库约 30 GB。为什么要分片？分几片，按什么分？

## A
**原因。** 版本切换时新旧两份同时在内存里，30 GB 的库切换峰值要 60 GB。

**做法。** 按前缀的哈希分成 4 片，每片约 7.5 GB，切换峰值约 15 GB；每次查询只访问一片。长度超过 12 个字符的长尾前缀不预存，在线取其 12 字符前缀的结果再按完整前缀过滤。
