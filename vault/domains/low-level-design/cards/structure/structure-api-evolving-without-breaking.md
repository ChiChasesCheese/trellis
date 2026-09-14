---
id: structure-api-evolving-without-breaking
node: structure.api
type: qa
---
## Q
Mid-round the interviewer keeps adding options to `search(String query)` — filters, sort, pagination. Name two evolution moves that don't break existing callers, and the smell if you don't.

## A
- **Parameter object**: `search(SearchQuery q)` where `SearchQuery` is a builder-built value object — new options become new optional fields, signature never changes again.
- **Overload delegation**: keep `search(String)` and have it delegate to the richer form with defaults (in interfaces, a `default` method does the same job).

The smell you're avoiding: a growing positional list `search(q, filter, sort, page, size, asc…)` where every addition breaks call sites and `null` gets passed for "don't care."


## Q zh
中间轮次面试官保持添加选项到 `search(String query)` — 筛选、排序、分页。命名两个不打破现有调用者的演化移动，以及如果你不这样做的味道。

## A zh
- **参数对象**: `search(SearchQuery q)` 其中 `SearchQuery` 是一个构造器构建的值对象 — 新选项变成新可选字段，签名永不再改变。
- **重载委托**: 保持 `search(String)` 并有它委托到更丰富的形式加上默认值（在接口中，一个 `default` 方法做同样的工作）。

你在避免的味道: 一个增长的位置列表 `search(q, filter, sort, page, size, asc…)` 其中每一个添加打破调用站点和 `null` 被传递为"不在乎"。
