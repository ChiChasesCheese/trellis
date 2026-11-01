---
id: hi-pt-tt-wallet-ledger-service-8-multi-currency
node: tt.sd.tt-wallet-ledger-service.points
type: qa
step: 8
---
## Q
**钱包与复式账本服务 · 多币种与换汇**｜出自：钱包与复式账本服务 › 深入 2

钱包支持美元、林吉特、平台金币，换汇时借贷相等怎么成立？

## A
**币种内守恒。** 借贷相等每个币种分别成立，不同币种的分录不放进同一个集合；换汇通过 FX 中间账户写成两组各自平衡的分录。
**例。** 100.00 USD 按 4.2135 换林吉特：USD 一侧借 user:USD 10,000 美分、贷 fx_position:USD；MYR 一侧借 fx_position:MYR 42,135、贷 user:MYR。
**落账。** 报价编号、原币、目标币、汇率一起落账，不能事后用当天汇率反算；点差 1.65 林吉特进收入账户。
