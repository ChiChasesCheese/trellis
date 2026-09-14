---
id: cc-round-submit-format-recheck
node: round.submission
type: qa
---
## Q
How do you check your output format in the last five minutes — and how do you not check it?

## A
**Byte-compare against the given sample; do not eyeball it.**

```bash
python3 sol.py < sample_input | diff - expected_output && echo SAME
```

Eyeballing misses exactly the things graders test: a space after the comma or not, `-3.5` where `-3.50` is required, an upper-case sentinel, a header line printed on empty input, a missing final newline. If the round gives no expected-output file, hand-write the expected lines from the worked example into a file first — writing them out is itself the check.

## Q zh
最后五分钟怎么检查输出格式 —— 以及不该怎么检查？

## A zh
**和给定样例逐字节比对；不要用眼睛看。**

```bash
python3 sol.py < sample_input | diff - expected_output && echo SAME
```

肉眼恰好会漏掉评测机要测的东西：逗号后有没有空格、需要 `-3.50` 却写成 `-3.5`、sentinel 的大小写、空输入时多打了表头、少了末尾换行。如果这一轮没给期望输出文件，就先按样例把期望的每一行手写进一个文件 —— 写出来这个动作本身就是检查。
