---
id: cc-verification-tests-worked-example-first
node: verification.tests
type: qa
---
## Q
You have 60 minutes and the statement includes three worked examples. What is the first code you write after the parser, and why not later?

## A
**The worked example, verbatim, as an executable test** — input and expected output copied character for character before you write a single rule.

- It pins the output contract (separators, decimal places, sentinel words) at minute 10 instead of minute 55, which is the cheapest way to stop failing on format.
- It is the only expected output you did not compute yourself, so it is the only one that can disagree with your reading of the spec.
- Copy, do not retype: "tidying" a double space or a trailing comma silently changes the contract.
- If the prose and the example conflict, the example wins — and the conflict is an assumption worth writing down.

## Q zh
你有 60 分钟，题面给了三个样例。写完解析器之后你写的第一段代码是什么？为什么不能往后放？

## A zh
**把样例原样做成可执行测试** —— 输入和期望输出逐字符照抄，在你写下第一条规则之前。

- 它把输出契约（分隔符、小数位、哨兵词）钉死在第 10 分钟而不是第 55 分钟，这是停止因格式失分的最便宜办法。
- 它是唯一一份不是你自己算出来的期望输出，因此也是唯一可能与你对题面的理解相抵触的那份。
- 要复制，不要重打：把双空格或结尾逗号「整理」掉，会悄悄改变契约。
- 如果正文和样例冲突，以样例为准 —— 而这个冲突值得作为一条假设记下来。
