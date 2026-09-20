---
id: structure-api-evolving-without-breaking
node: structure.api
type: qa
step: 2
---
## Q
面试中途面试官不断给 `search(query)` 加选项——过滤、排序、分页。怎样演化这个签名而不打破已有调用方？

## A
用**参数对象（parameter object）**：`search(q: SearchQuery)`，`SearchQuery` 是一个 `@dataclass`，新选项变成它新增的、带默认值的字段——`search` 本身的签名永远不用再改。要保留旧的简单调用方式，可以让旧签名成为一个便捷包装：`def search(query): return search(SearchQuery(query))`。

要避开的坏味道：`search(q, filter, sort, page, size, asc=True)` 这种不断增长的位置参数列表——每加一个新维度都会打破所有调用点，还逼着中间的调用方传 `None` 表示"不关心"。
