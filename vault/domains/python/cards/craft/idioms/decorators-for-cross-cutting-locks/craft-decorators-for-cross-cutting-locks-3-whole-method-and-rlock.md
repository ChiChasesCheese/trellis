---
id: craft-decorators-for-cross-cutting-locks-3-whole-method-and-rlock
node: craft.idioms.decorators-for-cross-cutting-locks
type: qa
step: 3
---
## Q
**装饰器做横切关注点 · 账本为什么用 RLock，什么情况下整个方法加锁行不通**｜写法

账本的 `reverse`（冲正）要调用 `post`（写入分录）。两个方法都被装饰器包在同一把锁里。用普通 `Lock` 会怎样？为什么账本用 `RLock`？还有什么场景下「整个方法一个临界区」是错的选择？

## A
**要点。** 普通锁（`Lock`）不可重入：同一个线程持有时再拿一次，会永远等自己，死锁。`RLock`（可重入锁，reentrant lock）记录持有者和次数，同一线程可以重复拿。当加了锁的公开方法会互相调用时，用 `RLock` 最省事。更干净的做法是把真正的逻辑放在不加锁的内部方法 `_post`，两个公开方法都只负责拿锁再调它。

```python
def make(lock):
    def synchronized(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            with lock:
                return method(self, *args, **kwargs)
        return wrapper
    return synchronized

def try_run(lock_kind):
    lock = lock_kind()
    sync = make(lock)

    class Ledger:
        @sync
        def post(self, n):
            return n

        @sync
        def reverse(self, n):
            return -self.post(n)        # 在持锁时调用另一个同样加锁的方法(重入)

    # 在另一个线程里试, 避免真的卡死主线程
    out = []
    t = threading.Thread(target=lambda: out.append(Ledger().reverse(5)), daemon=True)
    t.start(); t.join(0.5)
    return out[0] if out else "死锁(0.5 秒内没有返回)"

print("Lock :", try_run(threading.Lock))
print("RLock:", try_run(threading.RLock))
```

实际输出：

```
Lock : 死锁(0.5 秒内没有返回)
RLock: -5
```

**不适用的场景。** 方法体里需要**在中途释放锁**去做慢事或调外部代码：回调监听者、发网络请求、等待别的线程。整个方法一个临界区，这些都被持在锁里（见「锁内记事件、锁外派发」）。此时应把方法拆成两段：锁内改状态并记下事件，出锁后再派发，装饰器只包前一段。

**代价。** RLock 的重入会掩盖设计问题：回调里重入账本，看到的是改了一半的状态而不是死锁，错误更难发现。能拆就拆成无锁的内部方法，不要靠重入。
