---
id: problems-digital-wallet-why-not-saga-for-core-transfer
node: problems.commerce.digital-wallet
type: qa
step: 3
tags: [grown]
---
## Q
In a digital wallet, why is a saga (local transactions plus compensating actions) unsuitable for the core wallet-to-wallet money movement itself, even though it's fine for side effects like notifications or loyalty points?

## A
A saga commits each local step immediately and only compensates afterward on failure, which means intermediate state is visible to other transactions by design — the sender's debit can be visible to a balance read before the receiver's credit lands, or before a later compensation reverses it. A wallet transfer's requirement that a balance query after a transfer always reflects a consistent outcome (never a half-done state) rules this out for the money movement itself. Sagas remain the right tool for orchestrating non-transactional side effects that sit outside the transfer (sending a notification, awarding loyalty points), because those steps don't need to preserve the no-visible-intermediate-state guarantee that account balances do.

## Q zh
在数字钱包设计中，为什么 saga（本地事务加补偿动作）不适合用在核心的钱包间资金移动本身，尽管它适合用在通知、积分这类副作用上？

## A zh
saga 立即提交每个本地步骤，只在失败后才做补偿，这意味着中间状态本来就会被其他事务读到——发起方的扣款可能在接收方到账之前、或在后续补偿撤销它之前就被余额查询读到。而钱包转账要求转账后的余额查询必须始终反映一个一致的结果（绝不能是半途而废的状态），这就排除了把 saga 用在资金移动本身上。saga 仍然适合编排转账之外的非事务性副作用（发通知、加积分），因为这些步骤不需要保持账户余额那种“不允许可见中间态”的保证。
