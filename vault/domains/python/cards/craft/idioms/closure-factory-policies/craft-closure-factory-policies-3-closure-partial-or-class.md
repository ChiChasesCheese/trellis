---
id: craft-closure-factory-policies-3-closure-partial-or-class
node: craft.idioms.closure-factory-policies
type: qa
step: 3
---
## Q
**闭包工厂做策略 · 闭包、partial、带 __call__ 的类怎么选**｜写法

同一个「按百分比退款」的策略，可以写成闭包、`functools.partial`、或带 `__call__` 的小类。三者调用时没有区别，什么时候选哪个？这里面最容易在生产里出问题的差别是什么？

## A
**要点。** 三者调用方式相同，差别在调用之外：能不能看（repr）、能不能传出进程（pickle）、能不能放状态和多个方法。无状态且只在本进程使用：闭包最省。要打印、记日志、跨进程发送：partial 或类。有状态或有第二个方法：类。

```python
def percent(p):                          # 闭包
    def f(fare): return fare * p // 100
    return f

def pct(p, fare): return fare * p // 100

@dataclass(frozen=True)                  # 小类
class Percent:
    p: int
    def __call__(self, fare: int) -> int: return fare * self.p // 100

for name, obj in [("closure", percent(50)), ("partial", partial(pct, 50)), ("class", Percent(50))]:
    try:
        pickle.dumps(obj); ok = "ok"
    except Exception as e:
        ok = type(e).__name__
    print(f"{name:8} pickle={ok:14} repr 带参数={'50' in repr(obj)}")
```

实际输出（Python 3.14；报错文字在 3.11 里略有不同）：

```
closure  pickle=PicklingError  repr 带参数=False
partial  pickle=ok             repr 带参数=True
class    pickle=ok             repr 带参数=True
```

**为什么。** 闭包是局部定义的函数，pickle 按名字找函数，找不到。所以把闭包策略交给 `multiprocessing` 的工作进程、或存进需要序列化的缓存，会在运行时才失败。闭包的 repr 也只显示 `<function percent.<locals>.f ...>`，日志里看不出是哪一档。

**信号。** 策略开始需要「记住上一次」（滑动窗口、计数、缓存），或者需要 `reset()` 之类第二个方法：改成类，别在闭包里用 `nonlocal` 硬撑。
