---
id: craft-seams-for-testing-4-inject-not-patch
node: craft.architecture.seams-for-testing
type: qa
step: 4
---
## Q
**测试接缝 · 为什么时钟要作为参数传入，而不是 mock.patch 全局时间**｜架构

限流器需要「当前时间」。测试里用 `mock.patch("time.time")` 来快进，和构造限流器时传入一个 `clock` 函数，看起来都能做到。后来实现把 `time.time` 改成了 `time.monotonic`，两种测法分别会怎样？

## A
**要点。** `patch` 绑定的是被测代码内部用了哪个全局函数这个实现细节：实现换了调用，测试不会报错也不会提醒，只是悄悄失去快进能力，更糟的是断言可能照样绿着。注入（injection）把时钟作为构造参数，是对外的接口，实现怎么用时间由它自己决定，测试给什么时间它就是什么时间。

```python
class Limiter:
    def __init__(self, limit, window):
        self.limit, self.window, self.hits = limit, window, []
    def _allow(self, now):
        self.hits = [h for h in self.hits if h > now - self.window]
        if len(self.hits) >= self.limit:
            return False
        self.hits.append(now)
        return True
    def allow(self):
        return self._allow(time.monotonic())    # 直接读全局时间（实现早就从 time.time 换成了 monotonic）

class InjectedLimiter(Limiter):
    def __init__(self, limit, window, clock):
        super().__init__(limit, window)
        self.clock = clock                      # 时钟是参数
    def allow(self):
        return self._allow(self.clock())

lim = Limiter(1, 10)
with mock.patch("time.time", return_value=1000.0):
    print("第一次:", lim.allow())
with mock.patch("time.time", return_value=1011.0):      # 测试以为快进了 11 秒
    print("patch 快进后:", lim.allow())

t = [0.0]
lim2 = InjectedLimiter(1, 10, lambda: t[0])
print("注入时钟第一次:", lim2.allow())
t[0] = 11.0
print("注入时钟快进后:", lim2.allow())
```

限流 1 次/10 秒，各先放行一次，再「快进 11 秒」，实际输出：

```
第一次: True
patch 快进后: False
注入时钟第一次: True
注入时钟快进后: True
```

**为什么。** 第二行本该是 `True`：patch 的是旧函数，限流器读的是 `monotonic`，窗口没过，测试拿到 `False`；如果这条测试期望的恰好是「被限流」，它还会误报通过，隐藏问题。

**代价。** 注入要在构造函数里多一个参数，默认值给真实时钟即可；同理文件系统、`sleep` 也各开一个参数。
