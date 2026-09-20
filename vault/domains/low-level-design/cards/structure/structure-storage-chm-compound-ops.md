---
id: structure-storage-chm-compound-ops
node: structure.storage
type: qa
step: 4
---
## Q
用一个 `dict` 加一把 `threading.Lock` 做钱包余额存储，为什么 `balances[user] = balances[user] + amount` 这一行本身仍然可能丢钱？正确的写法是什么？

## A
`dict` 的**单次**读或写操作（`__getitem__`、`__setitem__`）在 CPython 里因为 GIL，一个字节码内是原子的；但 `balances[user] = balances[user] + amount` 是"读取旧值 → 计算新值 → 写回"**三个独立步骤**的组合，GIL 只保证每一步各自原子，不保证整条语句作为一个整体不被切换出去。两个线程可能都读到旧余额 100，各自算出 100+x 再写回，其中一次充值就此丢失（丢失更新，lost update）。

正确写法是把"读改写"整体包进一把锁：

```python
with self._lock:
    balances[user] = balances.get(user, 0) + amount
```

如果一次操作要跨越**多个 key**（比如在两个用户的钱包之间转账），单把锁仍然管用，但要注意锁的获取顺序一致，否则会有死锁风险。
