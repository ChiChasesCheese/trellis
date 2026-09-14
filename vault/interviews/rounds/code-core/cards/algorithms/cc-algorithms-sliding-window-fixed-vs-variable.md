---
id: cc-algorithms-sliding-window-fixed-vs-variable
node: algorithms.sliding-window
type: cloze
---
A **fixed** window of size k needs no left pointer at all — the element leaving at step `i` is {{c1::`a[i - k]`}}, so the update is one add and one remove in O(1). A **variable** window needs a left pointer and a loop that shrinks while {{c2::the invariant is violated}}. A window over *timestamps* is variable even when the count is fixed, because the eviction test is {{c3::a comparison against `t - w`, not an index}} — and the events must be {{c4::sorted per key}} before either pointer means anything.

## zh
**定长**为 k 的窗口根本不需要左指针 —— 第 `i` 步离开的元素是 {{c1::`a[i - k]`}}，所以更新就是一加一减的 O(1)。**变长**窗口需要左指针，以及一个在 {{c2::不变式被破坏时}} 收缩的循环。基于*时间戳*的窗口即使数量固定也是变长的，因为驱逐判据是 {{c3::与 `t - w` 的比较，而不是下标}} —— 而且事件必须先 {{c4::按 key 排序}}，两个指针才有意义。
