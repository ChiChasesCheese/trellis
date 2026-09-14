---
id: cc-rules-money-float-symptom
node: rules.money
type: qa
---
## Q
If a float touches money, what does the failure actually look like in a graded run?

## A
**One test out of twenty fails by one cent, and nothing else looks wrong.**

The three mechanisms: `0.1 + 0.2 == 0.30000000000000004`, so an equality test against a total fails; summing 10^5 amounts accumulates error until a value lands on the wrong side of a rounding boundary; and `int(7.35 * 100)` is `734` because `7.35` is stored slightly below.

None of these show up on the sample, all of them show up on a large or adversarial input, and the diff is a single character. That asymmetry — invisible while developing, fatal when graded — is why the rule is absolute rather than a preference.

## Q zh
如果 float 碰到了钱，在评测中失败具体长什么样？

## A zh
**二十个测试里有一个差一分钱，其余一切看起来都正常。**

三种机制：`0.1 + 0.2 == 0.30000000000000004`，于是对总额的等值判断失败；把 10^5 个金额相加会累积误差，直到某个值落到取整边界的另一侧；以及 `int(7.35 * 100)` 等于 `734`，因为 `7.35` 存储时略小于真值。

这些在样例上都不显形，在大规模或对抗性输入上全都显形，而 diff 只差一个字符。正是这种不对称 —— 开发时看不见、评测时致命 —— 让这条规则是绝对的，而不是偏好。
