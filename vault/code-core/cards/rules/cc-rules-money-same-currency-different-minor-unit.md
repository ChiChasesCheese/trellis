---
id: cc-rules-money-same-currency-different-minor-unit
node: rules.money
type: qa
tags: [grown]
---
## Q
A payment processor treats the Hungarian Forint (HUF) as a two-decimal currency for charges — `amount: 1045` means 10.45 HUF — but as a zero-decimal currency for payouts, where a payout `amount` must be an integer evenly divisible by 100 (you can pay out 10.00 HUF as `1000`, but never the full balance of 10.45 HUF). What does this tell you about where a currency's 'minor unit' actually lives, and how should a lookup table be keyed?

## A
The minor unit is not a fixed property of the currency code by itself — backward-compatibility and settlement-rail constraints can override a currency's 'natural' decimal count for one kind of operation while leaving it unchanged for another, on the very same currency. A table keyed only on currency (`{"huf": 0}` or `{"huf": 2}`) is wrong for HUF no matter which value you pick, because charges and payouts disagree. The lookup has to be keyed on (currency, operation), and any leftover fraction that doesn't fit the coarser operation's granularity (10.45 − 10.00 = 0.45 HUF) must be handled explicitly — credited back or reported — rather than silently dropped by truncation.

## Q zh
某支付处理商在处理 charge（收款）时把匈牙利福林（HUF）当作两位小数的货币——`amount: 1045` 表示 10.45 HUF——但在处理 payout（打款）时却把它当作零位小数的货币，payout 的 `amount` 必须是能被 100 整除的整数（你可以把 10.00 HUF 作为 `1000` 打出去，但永远无法把 10.45 HUF 的全部余额打出去）。这说明一种货币的"minor unit（最小单位）"到底取决于什么？查表时应该以什么作为 key？

## A zh
minor unit 并不是货币代码本身固定不变的属性——向后兼容性和结算通道的约束，可以在同一种货币上，对某一类操作覆盖掉它"天然"的小数位数，而对另一类操作保持不变。一张只以货币为 key 的表（`{"huf": 0}` 或 `{"huf": 2}`）无论选哪个值对 HUF 来说都是错的，因为 charge 和 payout 本身就不一致。查表必须以 (货币, 操作) 作为 key，而任何不满足较粗操作粒度的剩余小数（10.45 − 10.00 = 0.45 HUF）都必须被显式处理——记入余额或上报——而不能被截断悄悄丢弃。
