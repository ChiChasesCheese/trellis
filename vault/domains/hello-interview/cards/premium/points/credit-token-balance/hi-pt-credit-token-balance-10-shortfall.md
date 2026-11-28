---
id: hi-pt-credit-token-balance-10-shortfall
node: qb.lld.credit-token-balance.points
type: qa
step: 10
---
## Q
**额度账本 · 不够扣的语义**｜追问 · 出自：额度账本 › 深入 6

余额不够时，有的语义是整笔拒绝，有的是能扣多少扣多少。在这个设计里两者差在哪里？

## A
**整笔拒绝（核心）。** `_replay` 末尾 `if need: raise InsufficientCreditsError`，账本不变。

**尽力而为。** 删掉那两行，扣费只取到手的部分。实测：10 的包上扣 25 得 10、余额 0；迟到一个 5 的包后，同一笔扣费的分配变成 10 加 5。这种语义下账本不再拒绝任何扣费。

**先问清。** 面试开头就要问是哪一种。
