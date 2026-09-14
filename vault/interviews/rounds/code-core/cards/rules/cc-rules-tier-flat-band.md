---
id: cc-rules-tier-flat-band
node: rules.tiers
type: qa
---
## Q
A band carries a flat amount rather than a per-unit price. How is it charged in each pricing mode?

## A
**Once if any unit falls in the band — never multiplied by the quantity.**

- Volume: the whole quantity sits in one band, so a flat band charges its amount and nothing else. Quantity 3 in a flat band of 2500 costs 2500.
- Graduated: each band contributes; a flat band contributes its amount once as long as at least one unit falls inside it, then later bands price their own units. `1-1 flat 2500` plus `2+ @ 900` at quantity 3 is `2500 + 2 x 900 = 4300`.

The failure is treating `flat` as a unit price, which multiplies a setup fee by the order size — a large, obvious wrong answer that no rounding test would catch.

## Q zh
某个区间给的是固定金额而不是单价。在两种计价模式下各怎么收？

## A zh
**只要有任何单位落在该区间内就收一次 —— 绝不乘以数量。**

- volume：整个数量落在一个区间里，所以固定区间就只收它那个金额。数量 3 落在 2500 的固定区间里，收 2500。
- graduated：每个区间都贡献一部分；固定区间只要有至少一个单位落入就贡献一次它的金额，随后的区间再各自为自己的单位计价。`1-1 flat 2500` 加 `2+ @ 900`，数量 3 时是 `2500 + 2 x 900 = 4300`。

失败方式是把 `flat` 当成单价，于是把一笔开办费乘上了订单规模 —— 一个巨大而明显的错误答案，任何取整测试都抓不到它。
