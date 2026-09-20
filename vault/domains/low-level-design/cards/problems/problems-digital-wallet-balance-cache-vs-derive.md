---
id: problems-digital-wallet-balance-cache-vs-derive
node: problems.marketplaces.digital-wallet
type: qa
step: 4
tags: [grown]
---
## Q
在数字钱包（Digital Wallet）设计里，账户余额应该每次都从账本现算，还是缓存在账户上、定期用账本核对？为什么？

## A
本设计选择缓存并核对：`balance()` 只是一次字典查找加锁，O(1)；每次资金移动的同时在同一段临界区里更新缓存。查余额是钱包里被调用最频繁的操作（每次转账前、每次打开界面都要查），如果每次都从账本的全部历史分录现算（O(历史长度)），用了几年的账户会越查越慢。代价是缓存可能漂移，因此需要一个 `reconcile` 方法定期从账本重新推导真值、发现不一致就用账本覆盖缓存——账本永远是被信任的一方，缓存只是它的投影。
