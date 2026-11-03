---
id: craft-lazy-expiry-settle-on-access-2-settle-in-decorator
node: craft.patterns.lazy-expiry-settle-on-access
type: qa
step: 2
---
## Q
**惰性过期 · 把结清放进装饰器，防的是哪类 bug**｜模式

库存系统每个公开方法都要先把到期的预留释放，再读数字。如果每个方法开头手写 `self._expire_due()`，几个月后有人加了一个新方法 `available()`。会出什么问题？怎么让它不可能忘记？

## A
**要点。** 忘记结清的方法会读到「已经过期、本应释放」的预留，返回少算的可用量，而且没有任何报错，只在时间恰好跨过到期点时才出错，测试很难撞上。把「拿锁 + 结清」做成装饰器，套在每个公开方法上，规则就写在一处。

```python
def _op(method):                         # 每个公开方法：先拿锁，再结清，再做自己的事
    @wraps(method)
    def wrapper(self, *a, **k):
        with self._lock:
            self._expire_due()
            return method(self, *a, **k)
    return wrapper

@_op
def available(self) -> int:
    return self.free                     # 读到的数字永远已经算过期
```

5 件库存，预留了 3 件、刚好到期，手写版忘了结清与装饰器版对比：

```
手写   available() = 5
装饰器 available() = 8
```

**为什么。** 把「每个入口先做 X」变成结构，而不是约定。新方法只要贴上装饰器，就自动服从。

**易错。** 装饰器要在锁里调用结清，结清和方法体是同一个临界区；否则结清完成后、方法体执行前，又有别的线程改了状态。
