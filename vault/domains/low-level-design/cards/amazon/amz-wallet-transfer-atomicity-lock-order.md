---
id: amz-wallet-transfer-atomicity-lock-order
node: amazon.amz-wallet
type: qa
step: 4
tags: [grown]
---
## Q
在钱包设计里，A 转给 B 和 B 转给 A 同时发生会出什么错？怎么防？

## A
转账要同时锁两个账户。线程 1 先锁 A 再等 B，线程 2 先锁 B 再等 A，互相等待——死锁。固定加锁顺序：总是按账户 id 排序后再加锁，两个线程都先锁 id 小的，就不会互相等待。锁内做「检查余额、写两条分录」，保证不会出现只扣不加。
```python
def transfer(self, src, dst, amount):
    first, second = sorted((src, dst))
    with self._locks[first], self._locks[second]:
        if self._balance[src] < amount:
            raise InsufficientFunds(src)
        self._append(src, -amount)
        self._append(dst, +amount)
```
