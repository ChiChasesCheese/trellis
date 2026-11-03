---
id: craft-decorators-for-cross-cutting-locks-4-across-problems
node: craft.idioms.decorators-for-cross-cutting-locks
type: qa
step: 4
---
## Q
**装饰器做横切关注点 · 账本的 `@_synchronized` 和库存的 `@_op` 做的是同一件事吗**｜写法

两个装饰器都在方法外面套一层锁。库存的 `@_op` 在拿锁之后还多做了一步。多出来的这一步为什么也放在装饰器里？

## A
**要点。** 同一个骨架：拿锁，做一个前置步骤（可以为空），执行方法。库存的前置步骤是「结清已到点的预留」（`_expire_due`）：每个公开操作开始时，先把该过期的预留放回可售库存，然后读到的任何数字都已经算过期。放在装饰器里就保证了不会有哪个方法忘记先结清。

```python
# double-entry-ledger：整个方法一个临界区
def _synchronized(method: _F) -> _F:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    return wrapper  # type: ignore[return-value]

# inventory-management：拿锁 + 结清到点的预留，再做自己的事
def _op(method: _F) -> _F:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            self._expire_due()
            return method(self, *args, **kwargs)
    return wrapper  # type: ignore[return-value]
```

这对应「惰性过期」：不开后台线程定时清，而是在每次访问前顺手结清。装饰器让「每次访问前」不依赖程序员记住。顺序也重要：先拿锁再结清，结清本身就改状态，必须在锁里。

**见于。** double-entry-ledger、inventory-management。

**信号。** 一类的所有公开方法开头都重复同样的几行（拿锁、检查是否关闭、结清过期）；或者出现「某个方法忘了先……」的 bug。
