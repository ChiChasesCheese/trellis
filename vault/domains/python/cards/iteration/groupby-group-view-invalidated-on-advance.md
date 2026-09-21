---
id: groupby-group-view-invalidated-on-advance
node: iteration.itertools
type: qa
source: python-docs
---
## Q
`for k, group in groupby(data, key):` 循环里拿到的 `group` 子迭代器，能不能先存起来、等外层循环进入下一轮之后再去消费它？

## A
不能。每个 `group` 都是和 `groupby()` 对象共享同一个底层迭代器的视图，不持有自己独立的数据；外层循环一旦继续 `next()` 推进到下一个 key，上一个 `group` 能看到的数据就已经被跳过或耗尽了。如果分组结果要留到以后用，必须在拿到 `group` 的当下就用 `list(group)` 把它物化成列表保存下来。
