---
id: amz-wallet-balance-from-append-only-ledger
node: amazon.amz-wallet
type: qa
step: 3
tags: [grown]
---
## Q
在钱包设计里，余额是存一个字段，还是由流水推出来？转账在账本里记几条？

## A
账本只追加（append-only）：每条 `LedgerEntry(账户、变动额、类型、时间、转账号)`，永不修改。转账记两条同转账号的分录，一条 -100、一条 +100，全账本总和恒为 0，这是可校验的不变量。余额读流水求和是 O(n)，所以另存一个缓存余额字段，并提供 `reconcile`：缓存值必须等于流水求和，不等就是 bug。好处是任何一分钱都能追到来源。
