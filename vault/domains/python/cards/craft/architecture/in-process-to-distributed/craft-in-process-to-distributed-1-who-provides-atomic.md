---
id: craft-in-process-to-distributed-1-who-provides-atomic
node: craft.architecture.in-process-to-distributed
type: qa
step: 1
---
## Q
**从单进程到分布式 · 幂等字典放到两台服务器上就失效了吗**｜架构

单进程的幂等转账：一个字典记住已处理的键，一把锁保证「查有没有、占位」不被打断。服务扩成两台，客户端超时重试时负载均衡把重试打到另一台。每台继续用自己的字典和锁，会发生什么？应该改什么？

## A
**要点。** 语义不变（同键只执行一次），变的是「原子」由谁提供：进程内是一把锁，多机时锁管不到别的机器，必须把占位交给共享存储的原子操作：数据库唯一约束、Redis `SET NX`。每台机器自己的字典只是各自的记忆，互相不知道。

```python
class SharedStore:                # 共享存储：同一键只有一个调用能占位（SET NX / 唯一约束）
    """远端的共享存储：同一个键只有一个调用能成功占位（相当于 Redis SET NX、唯一约束）。"""
    def __init__(self) -> None:
        self._d: dict[str, str] = {}
        self._mu = threading.Lock()
    def set_if_absent(self, key: str, val: str) -> bool:
        with self._mu:
            return self._d.setdefault(key, val) == val

charges: list[str] = []

class LocalServer:                # 每台机器自己的字典 + 锁
    def __init__(self, name: str) -> None:
        self.name, self._seen, self._mu = name, set(), threading.Lock()
    def pay(self, key: str) -> None:
        with self._mu:
            if key in self._seen:
                return
            self._seen.add(key)
        charges.append(f"{self.name}扣款")

class SharedServer:
    def __init__(self, name: str, store: SharedStore) -> None:
        self.name, self._store = name, store
    def pay(self, key: str) -> None:
        if self._store.set_if_absent(key, self.name):   # 原子占位交给共享存储
            charges.append(f"{self.name}扣款")

a, b = LocalServer("A"), LocalServer("B")
a.pay("k1"); b.pay("k1")                            # 客户端重试被负载均衡打到另一台
print("各用本机字典:", charges)
charges.clear()
store = SharedStore()
a, b = SharedServer("A", store), SharedServer("B", store)
a.pay("k1"); b.pay("k1")
print("共享存储占位:", charges)
```

同一个键先打到 A 再打到 B，两种服务器各跑一次，实际输出：

```
各用本机字典: ['A扣款', 'B扣款']
共享存储占位: ['A扣款']
```

**为什么。** 锁是进程内的约定，只对同一进程的线程有效；多机要靠一个所有人都得服从的仲裁者。每把进程内的锁在生产里都能对应一个机制：键表 → 唯一约束，扣款锁 → 账户行锁或数据库事务。

**代价。** 仲裁者成了网络上的依赖：它慢、不可达、超时的时候，调用方不知道占位到底成没成，所以请求还要带幂等键、客户端要重试到得到明确的答案。
