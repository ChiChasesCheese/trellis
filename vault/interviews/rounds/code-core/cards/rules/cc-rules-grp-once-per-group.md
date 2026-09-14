---
id: cc-rules-grp-once-per-group
node: rules.grouping
type: qa
---
## Q
A bonus applies "to a customer who has three or more transactions at the same merchant". A pair has five transactions. How many times is the bonus applied?

## A
**Whatever the statement says — and the two readings differ by a factor of five, so this is the sentence to re-read.**

- *Per qualifying row*: the 3rd, 4th and 5th transactions each add → three applications.
- *Once per group*: the pair qualifies, the bonus is added once, no matter how many rows.

The reported number-one failure in scoring problems is applying a group rule per row when it was meant once per group. Decide, then make the structure say it: iterate `for key, rows in groups.items()` for a once-per-group rule, and iterate rows for a per-row rule. Mixing the two shapes is how the bug survives review.

## Q zh
某项奖励适用于「在同一商户有三笔或以上交易的顾客」。某个组合有五笔交易。奖励被应用几次？

## A zh
**按题面说的算 —— 而两种读法相差五倍，所以这句话值得重读。**

- **每条符合条件的行各一次**：第 3、4、5 笔各加一次 → 三次。
- **每组一次**：该组合符合条件，奖励只加一次，与行数无关。

计分类题目里被报告最多的头号失败，就是把"每组一次"的规则按行应用。先决定，再让结构说出这个决定：每组一次的规则就写 `for key, rows in groups.items()`，按行的规则就遍历行。两种形状混用，正是这个 bug 能挺过 review 的原因。
