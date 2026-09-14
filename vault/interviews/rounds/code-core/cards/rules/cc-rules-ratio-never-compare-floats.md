---
id: cc-rules-ratio-never-compare-floats
node: rules.exact-ratio
type: qa
---
## Q
Why is `if fraud / total >= 0.25:` wrong even though it looks right and passes the sample?

## A
**Because neither side is the number you wrote.** `0.25` happens to be exact in binary, but `0.1`, `0.34` and `0.7` are not, and `fraud / total` introduces its own rounding — so the comparison at the exact boundary is decided by representation error rather than by the rule.

That boundary is precisely the case a grader tests: a merchant sitting at exactly 1 of 4, or 1 of 3 against `0.33`.

The workaround people reach for — an epsilon — makes it worse: it turns an exact rule into an approximate one and now fails a *different* boundary test. Compare integers. See [[cc-rules-ratio-cross-multiply]].

## Q zh
为什么 `if fraud / total >= 0.25:` 是错的 —— 尽管它看起来没问题，也能通过样例？

## A zh
**因为两边都不是你写下的那个数。** `0.25` 恰好在二进制里精确，但 `0.1`、`0.34`、`0.7` 不是，而 `fraud / total` 又引入了自己的舍入 —— 于是恰好在边界处的比较，是由表示误差而不是由规则决定的。

而那个边界正是评测机要测的用例：恰好 4 笔中 1 笔的商户，或者 3 笔中 1 笔对上 `0.33`。

人们常用的补救 —— 加一个 epsilon —— 只会更糟：它把精确规则变成近似规则，于是换成另一个边界测试失败。请比较整数。见 [[cc-rules-ratio-cross-multiply]]。
