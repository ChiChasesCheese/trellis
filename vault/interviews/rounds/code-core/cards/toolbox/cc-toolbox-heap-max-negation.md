---
id: cc-toolbox-heap-max-negation
node: toolbox.heap
type: cloze
---
`heapq` builds min-heaps only, so a max-heap is {{c1::push `(-value, ...)` and negate again on pop}}. You cannot negate a string, so "largest amount, ties by smallest name" is {{c2::`(-amount, name)`}} while "largest amount, ties by *largest* name" has no tuple key at all — that one needs {{c3::a wrapper class defining `__lt__`}}. For a one-shot selection, {{c4::`heapq.nlargest(k, xs, key=...)`}} avoids the negation entirely.

## zh
`heapq` 只能建小顶堆，所以大顶堆的做法是 {{c1::push `(-value, ...)`，pop 时再取负}}。字符串不能取负，所以「金额最大，并列取名字最小」是 {{c2::`(-amount, name)`}}，而「金额最大，并列取名字*最大*」根本没有 tuple key —— 那种情况需要 {{c3::一个定义了 `__lt__` 的包装类}}。若只做一次性选取，{{c4::`heapq.nlargest(k, xs, key=...)`}} 可以完全避开取负。
