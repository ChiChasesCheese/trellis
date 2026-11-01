---
id: hi-pt-tt-double-entry-ledger-9-fx
node: tt.lld.tt-double-entry-ledger.points
type: qa
step: 9
---
## Q
**复式账本（类设计） · 跨币种转账**｜出自：复式账本（类设计） › 取舍与追问

追问：跨币种转账怎么记？

## A
**做法。** 用两组各自平衡的腿，经 FX 中间账户：用户美元账户减少、FX 中间账户美元增加；FX 中间账户林吉特减少、对方林吉特账户增加。
**记录。** 分录里记汇率和报价编号，汇兑差额进汇兑损益账户，不要悄悄吃掉。
