---
id: amz-locker-onsite-notepad-at-minute-20
node: amazon.amz-locker-onsite
type: qa
step: 2
tags: [grown]
---
## Q
在 Amazon 现场版快递柜里，写到第 20 分钟时，记事本（不运行的代码）上至少应有什么？

## A
三个数据类（尺寸、柜格、授权）加一个网点类，且 `deposit` 与 `collect` 的主路径写完整，失败路径用具名异常。时钟、有效期由构造函数传入，不在方法里取现在时间。
```python
def deposit(self, pkg):
    with self._lock:
        fits = [l for l in self._free if l.size.holds(pkg.size)]
        if not fits:
            raise NoLockerAvailable(pkg.id)
        locker = min(fits, key=lambda l: l.size.volume)
        self._free.remove(locker)
        code = self._new_code()
        expires = self._clock() + self._ttl
        self._grants[code] = Grant(locker, pkg, expires)
        return code
```
