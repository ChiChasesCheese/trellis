---
id: cc-algorithms-binary-search-bounds
node: algorithms.binary-search
type: cloze
---
The bounds must bracket the answer, or the loop returns a boundary that {{c1::is not a real answer}}. Set `lo` to the smallest legal value and `hi` to something {{c2::provably feasible}} — for "minimum capacity to ship everything" that is {{c3::the largest single item}} for `lo` and {{c4::the sum of all items}} for `hi`. On a half-open index search, `hi = n` is deliberate: the return value {{c5::n}} then means "no index satisfies the predicate", which is a legitimate answer rather than an error.

## zh
上下界必须夹住答案，否则循环返回的边界 {{c1::根本不是一个真实答案}}。把 `lo` 设为最小的合法值，把 `hi` 设为 {{c2::可证明可行}} 的值 —— 对「运完所有货物所需的最小运力」来说，`lo` 是 {{c3::最大的单件货物}}，`hi` 是 {{c4::所有货物之和}}。在半开区间的下标搜索里，`hi = n` 是有意为之：返回值 {{c5::n}} 表示「没有下标满足谓词」，这是合法答案而非错误。
