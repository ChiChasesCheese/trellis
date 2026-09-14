---
id: cc-model-ev-passes-vs-interleaved
node: model.event-stream
type: qa
---
## Q
Three scoring rules must be applied to a list of transactions. The statement says "three separate passes over the whole list". Why is that not the same as applying all three inside one loop?

## A
**Because a multiplicative rule applied in pass 1 multiplies the base score only, while the same rule inside one interleaved loop multiplies whatever the additive rules have already added.**

```
base 10, txn A adds 5, txn B multiplies by 2
three passes : (10 * 2) + 5 = 25
interleaved  : (10 + 5) * 2 = 30
```

Non-commuting operations make pass structure part of the specification, not an implementation choice. Read "passes" literally, write one function per pass, and keep the order the statement gives — including that pass k sees *every* transaction before pass k+1 starts.

## Q zh
三条计分规则要应用到一个交易列表上。题面说「对整个列表分三趟」。为什么这和"在一个循环里同时应用三条"不同？

## A zh
**因为在第一趟里应用的乘法规则只乘基础分，而同一条规则放进单个交错循环里，乘的是加法规则已经加上去之后的值。**

```
base 10, txn A adds 5, txn B multiplies by 2
three passes : (10 * 2) + 5 = 25
interleaved  : (10 + 5) * 2 = 30
```

不可交换的运算让"分趟"成为规格的一部分，而不是实现选择。把「pass」照字面读，每趟写一个函数，并保持题面给的顺序 —— 包括第 k 趟要走完**所有**交易，第 k+1 趟才开始。
