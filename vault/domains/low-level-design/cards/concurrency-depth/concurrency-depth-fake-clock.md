---
id: concurrency-depth-fake-clock
node: concurrency-depth.testing
type: qa
step: 5
---
## Q
限流器“窗口 100 秒、放行 1 次”怎么测边界：t=0 放行、t=50 拒绝、t=100 放行？为什么不用 `time.sleep`？

## A
**把时钟注入进去，测试里手动拨表**

- **`sleep` 的问题**：测 100 秒的窗口要睡 100 秒；缩成 0.1 秒的窗口，机器一忙，睡的时间和你以为的不一样，边界断言偶尔红；
- **做法**：被测对象接受一个 `clock` 参数（示例里是必填，生产代码可以默认 `time.monotonic`），测试传一个可以手动拨动的假时钟，时间由测试决定，毫秒级跑完且每次相同；
- **边界要单独测**：恰好满一个窗口（t=100）放不放行，是规格要问清的地方，测试把它写死；
- **同样的想法用到顺序上**（示例没有）：要让任务 B 先于任务 A 完成，用 `Event` 链：B 完成后 `set()`，A 等这个事件才继续，不靠谁睡得更久；
- **假时钟只在测试线程里拨**：被测代码读它，测试代码写它；多线程一起拨表，这个测试自己就成了竞态。

```python
class Once:                                      # 一个窗口内只放行一次
    def __init__(self, window, clock):
        self.w, self.clock, self.last = window, clock, None
    def check(self):
        now = self.clock()
        if self.last is None or now - self.last >= self.w:
            self.last = now
            return True
        return False

t = [0.0]
o = Once(100, lambda: t[0])
print(o.check())                                 # True（t=0）
t[0] = 50;  print(o.check())                     # False
t[0] = 100; print(o.check())                     # True（恰好一个窗口）
```

**知识点：**测试并发代码（Testing Concurrency）
