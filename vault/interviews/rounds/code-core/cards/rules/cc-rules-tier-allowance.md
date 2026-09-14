---
id: cc-rules-tier-allowance
node: rules.tiers
type: qa
---
## Q
A plan costs a flat fee and includes 40,000 tokens; usage beyond that is metered. What does the arithmetic have to pin down?

## A
**The order in which the allowance is consumed, and what happens exactly at the boundary.**

- Consumption order matters when overage is priced differently by kind: input tokens before output tokens, in session order, so the overage lands on the *later* and possibly dearer units.
- Exactly 40,000 billable tokens means zero overage — the allowance is inclusive.
- Any per-unit rounding (billing in blocks of 100) is applied **before** the allowance is drawn down, and again to the overage.

Write the three numbers out for one worked case — billable, consumed, overage — and check they sum.

## Q zh
某套餐收固定月费并包含 40,000 tokens；超出部分按量计费。这套算术必须钉死什么？

## A zh
**额度被消耗的顺序，以及恰好在边界上会发生什么。**

- 当超额部分按种类定价不同时，消耗顺序就要紧：先输入 token 后输出 token，按会话顺序，使超额落在**更靠后**、可能更贵的单位上。
- 恰好 40,000 个可计费 token 意味着超额为零 —— 额度是包含式的。
- 任何按单位的取整（按 100 为块计费）都要在扣减额度**之前**先做，然后对超额部分再做一次。

对一个算例把三个数字写出来 —— 可计费量、已消耗量、超额量 —— 并核对它们相加成立。
