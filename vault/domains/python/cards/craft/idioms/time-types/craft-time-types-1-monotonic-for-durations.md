---
id: craft-time-types-1-monotonic-for-durations
node: craft.idioms.time-types
type: qa
step: 1
---
## Q
**时间类型 · 限流窗口和租约为什么用 `time.monotonic`，不用当前时间**｜写法

限流器记下上次放行的时间，下次请求时算 `now - last` 看够不够间隔。如果 `now` 取自系统当前时间（`time.time()` 或 `datetime.now()`），机器做了一次 NTP 校时把时钟往回拨了一小时，会发生什么？

## A
**要点。** 墙钟（wall clock）会被系统校时、手工调整、闰秒改变，可能前跳也可能倒退。拿它算**时长**就不可靠：倒退时 `now - last` 变成负数，永远小于间隔，窗口里的请求被拒绝一整个小时。`time.monotonic()` 是单调时钟（monotonic clock）：只往前走，不受校时影响，保证 `b >= a`。它的数值本身没有意义（不是日历时间，只能相减），所以只用来量**时长**：限流窗口、租约、超时、重试间隔。

```python
Clock = Callable[[], float]

class Window:
    """限流窗口：距上次放行不足 interval 秒就拒绝。"""
    def __init__(self, interval: float, clock: Clock) -> None:
        self.interval, self.clock, self.last = interval, clock, None

    def allow(self) -> bool:
        now = self.clock()
        if self.last is not None and now - self.last < self.interval:
            return False
        self.last = now
        return True

# 模拟墙钟：一次校时把它往回拨了 1 小时
class FakeWall:
    def __init__(self): self.t = 1_000_000.0
    def __call__(self): return self.t
    def step_back(self): self.t -= 3600

wall = FakeWall()
w = Window(60, wall)
print("t=0           放行:", w.allow())
wall.step_back()                       # NTP 校时：墙钟回拨 1 小时
for i in range(2):
    wall.t += 60
    print(f"回拨后 +{(i + 1) * 60} 秒  放行:", w.allow())
print("now - last =", wall.t - w.last, "秒: 负数 < interval, 之后一小时全被拒绝")

mono = time.monotonic
a, b = mono(), mono()
print("monotonic 永不倒退:", b >= a)
```

实际输出：

```
t=0           放行: True
回拨后 +60 秒  放行: False
回拨后 +120 秒  放行: False
now - last = -3480.0 秒: 负数 < interval, 之后一小时全被拒绝
monotonic 永不倒退: True
```

**为什么。** 选时间类型先问：我要的是「过了多久」还是「现在是几号几点」。前者要单调性，后者要日历含义；两个需求不要共用一个值。

**代价。** monotonic 不能持久化也不能跨机器比较：进程重启后它的起点就变了，所以过期时间要存进数据库时，存的是墙钟（带时区），启动后再换算成本地的单调时长。
