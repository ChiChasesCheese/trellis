---
id: cc-rules-tier-band-boundaries
node: rules.tiers
type: qa
---
## Q
Bands are given as `1-2`, `3-4`, `5-`. Which quantities do you test, and what does the open band imply?

## A
**Test 1, 2, 3, 4, 5 and something huge — every band edge on both sides.**

`max` is inclusive, so quantity 2 is in the first band and 3 in the second; the last band is open-ended and must accept any quantity without an upper check.

Two structural rules that fall out: the bands are contiguous starting at 1, so a gap or an overlap in the input is malformed data rather than a pricing decision; and a quantity beyond the last **closed** band has no price — that is an error to raise, not a zero to return. Quantity 0 is a legitimate input and costs nothing in either pricing mode.

## Q zh
区间给定为 `1-2`、`3-4`、`5-`。你测哪些数量？开放区间意味着什么？

## A zh
**测 1、2、3、4、5，再加一个极大值 —— 每个区间边界的两侧都测。**

`max` 是包含的，所以数量 2 属于第一段、3 属于第二段；最后一段是开放的，必须接受任意数量而不做上界检查。

由此得出两条结构性规则：区间从 1 开始且连续，因此输入里的空隙或重叠是脏数据而不是定价决策；以及超出最后一个**闭合**区间的数量没有价格 —— 那是要抛出的错误，而不是返回零。数量为 0 是合法输入，在两种计价模式下都收 0。
