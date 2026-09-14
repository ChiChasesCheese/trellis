---
id: cc-performance-amortized-append-doubling
node: performance.amortized
type: cloze
---
`list.append` is amortized O({{c1::1}}) because the backing array grows geometrically, so n appends cost O({{c2::n}}) in total even though individual appends copy. `list.insert(0, x)` and `list.pop({{c3::0}})` are O({{c2::n}}) each, so n of them are quadratic — collect then sort, or reach for a `deque`.

## zh
`list.append` 摊还是 O({{c1::1}})，因为底层数组按几何级数扩容，所以 n 次 append 总计 O({{c2::n}})，尽管个别 append 会发生复制。`list.insert(0, x)` 和 `list.pop({{c3::0}})` 各自是 O({{c2::n}})，做 n 次就是平方级 —— 要么先收集再排序，要么改用 `deque`。
