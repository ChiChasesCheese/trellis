---
id: problems-coffee-machine-counter-not-atomic
node: problems.machines.coffee-machine
type: qa
step: 4
tags: [grown]
---
## Q
咖啡机用 `self._served += 1` 统计做成功的杯数，多个出口并发写它。Python 的 GIL 能保证这一行安全吗？

## A
不能。`+= 1` 是『读—加—写』三步字节码，两个线程可以读到同一个旧值、各加一次、各写一次，结果只增加了 1，丢掉一次计数。GIL 只保证**单条字节码**不被打断，从来不保证一个表达式或一段『先查后改』是原子的——这正是并发里最容易被想当然放过的地方。所以计数器要有自己的一把小锁（和库存锁分开，因为它们守的是不同的数据）。同一条道理适用于库存的『检查够不够 → 扣减』：它也是先查后改，必须在同一把锁里做完。
