---
id: problems-atm-two-authorities
node: problems.machines.atm
type: qa
step: 1
tags: [grown]
---
## Q
在 ATM 取款机的设计里，账户余额和机器钞箱是两样东西。谁是余额的权威？ATM 被允许假设什么？

## A
银行是余额唯一的权威，ATM 什么都不能假设——它既不缓存余额，也不持有可写的账户对象。可执行的做法是把网络一侧抽成一个只有动作、没有 `get_account()` 的协议：`authenticate`、`balance`、`withdraw`、`deposit`、`reverse`。ATM 拿不到账户对象，『机器偷偷改余额』在类型层面就不可能发生；断网时它也只能拒单而不能先给钱。ATM 自己拥有的是另一条不变式——钞票守恒：装钞总额 = 钞箱 + 出钞口 + 回收箱 + 客户已取走。两个权威各守一条，取款则是一次跨越两者、没有事务可用的操作。
