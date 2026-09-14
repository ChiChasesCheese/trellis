---
id: cc-round-debug-stderr-only
node: round.debugging
type: cloze
---
In a graded round every debug print goes to {{c1::`sys.stderr`}}, never to stdout, because stdout is {{c2::the channel the grader byte-compares}} — one stray trace line fails every test in the part. `print(..., file=sys.stderr)` costs three tokens and survives to the boundary sweep; a `print()` you meant to delete does not. {{c3::Delete or guard them anyway before submitting}}, because a harness that captures both streams will still show them to a human reviewer.

## zh
在被评分的轮次里，所有调试输出都打到 {{c1::`sys.stderr`}}，绝不打到 stdout，因为 stdout 是 {{c2::评测机逐字节比对的通道}} —— 一行漏掉的 trace 就能让这一部分的测试全挂。`print(..., file=sys.stderr)` 只多三个 token，而且能撑到边界扫查阶段；一个你打算删掉的 `print()` 撑不到。{{c3::提交前仍然要删掉或加开关}}，因为同时捕获两个流的评测系统还是会把它们展示给人类 reviewer。
