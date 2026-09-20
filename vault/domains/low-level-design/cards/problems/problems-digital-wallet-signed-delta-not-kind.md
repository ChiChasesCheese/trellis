---
id: problems-digital-wallet-signed-delta-not-kind
node: problems.marketplaces.digital-wallet
type: qa
step: 3
tags: [grown]
---
## Q
在数字钱包的双分录账本里，一条分录表示方向和金额时，为什么优先用一个带符号的整数 `delta`，而不是教科书式的 `kind`（DEBIT/CREDIT 枚举）加一个非负 `amount`？

## A
`kind` 和 `amount` 合在一起才能表达“这条分录让余额变化了多少”，两者必须永远保持一致；一旦某处赋值忘了同步更新 `kind`，账目会悄悄算错而不抛任何异常——这是最难排查的一类 bug。用带符号的 `delta`（正数入账、负数出账）把方向和大小压进同一个数字，“两条分录相加为零”就成了一行加法就能验证的不变式，不需要再核对符号和枚举值是否互相矛盾。这也是“该用 Enum、这里其实不需要”的一个具体判据：方向已经被符号完整表达时，多一个 Enum 字段是冗余而不是清晰。
