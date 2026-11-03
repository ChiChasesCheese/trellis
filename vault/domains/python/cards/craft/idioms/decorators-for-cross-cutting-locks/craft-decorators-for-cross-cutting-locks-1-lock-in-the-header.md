---
id: craft-decorators-for-cross-cutting-locks-1-lock-in-the-header
node: craft.idioms.decorators-for-cross-cutting-locks
type: qa
step: 1
---
## Q
**装饰器做横切关注点 · 为什么「整个方法加锁」写成装饰器，而不是每个方法里一个 `with`**｜写法

账本类有十来个公开方法，每个都要在锁里运行。每个方法体里写 `with self._lock:`，和给方法加一行 `@_synchronized`，差别在哪？

## A
**要点。** 横切关注点（cross-cutting concern）是跟业务无关、却要出现在很多方法里的东西：加锁、结清过期、记日志。写在每个方法里，规则靠人记：新加一个方法忘了加锁，就是一个只在并发下才出错的 bug。装饰器把规则挪到方法头上，锁的作用域在一眼就能看全的位置，漏了哪个方法，扫一遍 `@` 就能发现。

```python
class Account:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.held_when: dict[str, bool] = {}       # 每个方法运行时是否持有锁
        self.balance = 0

    def _probe(self, name: str) -> None:
        self.held_when[name] = self._lock.locked()

    def deposit(self, n: int) -> None:
        with self._lock:                            # 手写: 每个方法自己拿锁
            self._probe("deposit")
            self.balance += n

    def withdraw(self, n: int) -> None:
        with self._lock:
            self._probe("withdraw")
            self.balance -= n

    def reverse(self, n: int) -> None:
        self._probe("reverse")                      # 新来的方法, 忘了拿锁
        self.balance -= n

a = Account()
a.deposit(10); a.withdraw(3); a.reverse(1)
print("运行时是否持有锁:", a.held_when)
```

实际输出：

```
运行时是否持有锁: {'deposit': True, 'withdraw': True, 'reverse': False}
```

**为什么。** 手写版的 `reverse` 没有拿锁，却不会有任何报错，测试单线程跑也通过。装饰器版虽然也会有人忘记写 `@`，但「要写什么」缩成了一个固定的单词，漏掉更容易被代码评审或一个遍历公开方法的测试发现。

**代价。** 整个方法都在锁里，读起来像细粒度的锁，实际上是粗粒度的；方法中途想释放锁去调外部代码做不到（见第 3 张卡）。装饰器让加锁变得隐形，读者要知道每个公开方法被包了一层。
