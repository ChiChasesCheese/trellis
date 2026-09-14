---
id: cc-round-comm-questions-that-pay
node: round.communication
type: qa
---
## Q
You may ask a few clarifying questions before you start coding. Which questions are worth the minute they cost?

## A
**The ones whose answer changes code you would otherwise have to rewrite.**

Worth asking: the tie-break in the output order; is the threshold strict or inclusive; what is printed when the result is empty; can events arrive out of order; can an id be reused after it is closed.

Not worth asking: anything the statement already answers, or anything that does not change a line of code ("may I use a dict?").

Phrase each as a binary with your default attached — "I'll read *exceeds* as strict `>` unless you'd rather it be `>=`" — so a silent interviewer still leaves you unblocked.

## Q zh
开始写代码之前你可以问几个澄清问题。哪些问题值得它花掉的那一分钟？

## A zh
**答案会改变你否则就得重写的代码的那些问题。**

值得问：输出顺序的 tie-break；阈值是严格还是包含；结果为空时打印什么；事件会不会乱序到达；一个 id 关闭后能否被复用。

不值得问：题面已经回答的，或者不会改变任何一行代码的（「我可以用 dict 吗？」）。

每个问题都写成带默认值的二选一 —— 「我把 *exceeds* 读作严格的 `>`，除非你希望是 `>=`」 —— 这样即使面试官不表态，你也不会被卡住。
