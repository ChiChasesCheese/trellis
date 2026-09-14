---
id: cc-verification-edge-exact-threshold-triple
node: verification.edge-catalog
type: qa
---
## Q
A rule says "flag the merchant when the fraud count exceeds the limit". Your code passes the sample. What three inputs do you run, and why three?

## A
**One below, exactly at, one above** — `limit - 1`, `limit`, `limit + 1`.

- Only the middle input distinguishes `>` from `>=`, and it is precisely the value a worked example rarely contains.
- Run the triple for **every** threshold in the statement, including a minimum-volume gate and any ratio. Ratios need the same treatment in exact arithmetic: `1/2` against `0.5` is an exact hit, `1/3` against `0.33` is above, `1/3` against `0.34` is below.
- When the English is ambiguous ("exceeds", "at least", "more than"), the triple is also how you find out which reading the sample supports.
- Most boundary bugs live in the *second* threshold — the one nobody re-read.

## Q zh
规则说「当欺诈笔数超过上限时标记该商户」。你的代码通过了样例。你要跑哪三个输入？为什么是三个？

## A zh
**低一个、恰好等于、高一个** —— `limit - 1`、`limit`、`limit + 1`。

- 只有中间那个输入能区分 `>` 和 `>=`，而它恰恰是样例几乎不会包含的值。
- 对题面里的**每一个**阈值都跑这三元组，包括最低量门槛和任何比例。比例要用精确算术做同样的处理：`1/2` 对 `0.5` 是恰好命中，`1/3` 对 `0.33` 在上方，`1/3` 对 `0.34` 在下方。
- 当英文含糊时（"exceeds"、"at least"、"more than"），这三元组也是你查明样例支持哪种读法的手段。
- 大多数边界 bug 住在*第二个*阈值里 —— 那个没人回头重读的阈值。
