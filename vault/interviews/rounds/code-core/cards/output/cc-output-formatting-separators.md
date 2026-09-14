---
id: cc-output-formatting-separators
node: output.formatting
type: qa
---
## Q
One part's sample shows `m1, 42` and the next shows `m1,42`. Your code uses `", ".join(...)` everywhere. What is the discipline?

## A
**Copy the separator out of the sample, per line shape, and diff bytes.**

- One space after the comma versus none, a space around `->`, a trailing space at end of line, upper versus lower case tags — each of those is a whole failed test group, not a cosmetic issue.
- Reproduce the worked example **verbatim** before writing any case of your own, and compare with a byte diff, not by eye. Trailing whitespace is invisible in a terminal.
- Build the line with an f-string that mirrors the sample character for character rather than joining a list — a join hides the separator inside a helper.
- Trailing newline: `print()` emits exactly one and most graders tolerate it; emitting an extra **blank line** at the end is a different thing and usually fails.

## Q zh
一个 part 的样例是 `m1, 42`，下一个是 `m1,42`。而你的代码处处用 `", ".join(...)`。纪律是什么？

## A zh
**逐种行形态从样例里抄出分隔符，然后逐字节 diff。**

- 逗号后有没有空格、`->` 两侧的空格、行尾多余空格、标签大小写 —— 每一个都是整整一组测试失败，而不是外观问题。
- 在写自己的用例之前，先**逐字**复现题目给的样例，并用字节 diff 比对，而不是靠眼看。行尾空格在终端里是看不见的。
- 用与样例逐字符对应的 f-string 拼这一行，而不是 join 一个列表 —— join 会把分隔符藏进一个辅助函数里。
- 行尾换行：`print()` 恰好输出一个，多数 grader 能容忍；而在末尾多输出一个**空行**是另一回事，通常会失败。
