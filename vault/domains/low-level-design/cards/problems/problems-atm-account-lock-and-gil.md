---
id: problems-atm-account-lock-and-gil
node: problems.machines.atm
type: qa
step: 10
tags: [grown]
---
## Q
几台 ATM 同时对同一个账户取款。锁应该加在哪里？Python 的 GIL 能不能代替它？并发测试该断言什么？

## A
锁加在**账户**上：余额检查和扣减必须在同一把锁里一次做完（再加一条当日取现限额也落在同一把锁里，它是账户的第二条不变式）。GIL 代替不了它——`if amount > self.balance` 之后再 `self.balance -= amount` 是好几条字节码，两个线程可以同时通过那个 `if`，然后都去扣，余额变负；GIL 只保证单条字节码不被打断，不保证这段读-改-写原子。ATM 自己另有一把粗锁保护『查状态 → 查守卫 → 改状态』，粒度粗是对的：一台机器只有一个出钞口，本就没有并行度可榨。测试用 `threading.Barrier` 让线程同时起跑，断言的是不变式——恰好一个人取到钱、`余额 == 原余额 - 已出钞总额`——而不是任何时序或 `sleep`。
