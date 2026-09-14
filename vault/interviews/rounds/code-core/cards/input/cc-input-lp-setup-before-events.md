---
id: cc-input-lp-setup-before-events
node: input.line-protocols
type: cloze
---
When a statement says setup lines are applied {{c1::before any event, wherever they appear in the file}}, a single pass is wrong: a `THRESHOLD` line printed after the charges it governs would be read too late. The fix is {{c2::two passes over the same lines}} — collect configuration first, replay events second. The tell in a statement is a phrase like "wherever they appear" or {{c3::"the last one wins"}} for a repeated setup key.

## zh
当题面说配置行 {{c1::在任何事件之前生效，无论它们出现在文件的什么位置}} 时，单趟扫描就是错的：写在扣款之后的 `THRESHOLD` 行会被读得太晚。修法是 {{c2::对同一批行做两趟}} —— 先收集配置，再重放事件。题面里的信号是「wherever they appear」这类措辞，或者重复配置键的 {{c3::"the last one wins"}}。
