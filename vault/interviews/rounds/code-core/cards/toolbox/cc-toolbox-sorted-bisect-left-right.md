---
id: cc-toolbox-sorted-bisect-left-right
node: toolbox.sorted
type: cloze
---
On a sorted list containing duplicates, `bisect_left(a, x)` returns {{c1::the index of the first element >= x}} and `bisect_right(a, x)` returns {{c2::the index of the first element > x}}; their difference is {{c3::the number of occurrences of x}}. So "the latest entry written at or before `t`" is {{c4::`bisect_right(times, t) - 1`}} — a write exactly at `t` counts — while "strictly before `t`" is `bisect_left(times, t) - 1`. Both return {{c5::-1}} when nothing qualifies, which must be handled before indexing.

## zh
在含重复元素的有序列表上，`bisect_left(a, x)` 返回 {{c1::第一个 >= x 的元素的下标}}，`bisect_right(a, x)` 返回 {{c2::第一个 > x 的元素的下标}}；两者之差是 {{c3::x 的出现次数}}。于是「在 `t` 或之前写入的最新条目」是 {{c4::`bisect_right(times, t) - 1`}} —— 恰好写在 `t` 的也算 —— 而「严格早于 `t`」是 `bisect_left(times, t) - 1`。两者在无符合项时都返回 {{c5::-1}}，必须在取下标前处理掉。
