---
id: structure-api-evolving-without-breaking
node: structure.api
type: qa
---
## Q
中间轮次面试官保持添加选项到 `search(String query)` — 筛选、排序、分页。命名两个不打破现有调用者的演化移动，以及如果你不这样做的味道。

## A
- **参数对象**: `search(SearchQuery q)` 其中 `SearchQuery` 是一个构造器构建的值对象 — 新选项变成新可选字段，签名永不再改变。
- **重载委托**: 保持 `search(String)` 并有它委托到更丰富的形式加上默认值（在接口中，一个 `default` 方法做同样的工作）。

你在避免的味道: 一个增长的位置列表 `search(q, filter, sort, page, size, asc…)` 其中每一个添加打破调用站点和 `null` 被传递为"不在乎"。
