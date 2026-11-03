---
id: craft-decorators-for-cross-cutting-locks-5-scales-middleware
node: craft.idioms.decorators-for-cross-cutting-locks
type: qa
step: 5
---
## Q
**装饰器做横切关注点 · 从方法装饰器到服务的中间件，顺序为什么重要**｜写法

一个方法外面可以套多个装饰器：加锁、重试、追踪。放大到服务里，鉴权、限流、重试、追踪放在中间件（middleware），而不是每个 handler 手写。套的顺序有关系吗？

## A
**要点。** 有，而且是语义上的区别。多个装饰器是洋葱模型：先写的（最上面的）在最外层，请求从外往里穿过，响应从里往外返回。重试在外层，每次重试都会重新经过里面的追踪，留下多条记录；追踪在外层，整个操作（含所有重试）只算一次。服务中间件完全一样：限流放在鉴权之前还是之后，决定了未登录的请求会不会消耗限额。

```python
calls: list[str] = []

def tracing(name):
    def deco(fn):
        @wraps(fn)
        def w(*a, **k):
            calls.append(f"{name}.enter")
            try:
                return fn(*a, **k)
            finally:
                calls.append(f"{name}.exit")
        return w
    return deco

def retry(times):
    def deco(fn):
        @wraps(fn)
        def w(*a, **k):
            for i in range(times):
                try:
                    return fn(*a, **k)
                except RuntimeError:
                    if i == times - 1:
                        raise
        return w
    return deco

state = {"n": 0}
def flaky():
    state["n"] += 1
    if state["n"] < 3:
        raise RuntimeError("boom")
    return "ok"

# 洋葱模型: 先写的在外层。retry 在外 = 每次重试都被追踪一次; tracing 在外 = 整个操作只追踪一次
state["n"] = 0; calls.clear()
print(retry(3)(tracing("t")(flaky))(), calls.count("t.enter"), "次 enter  (retry 外层)")
state["n"] = 0; calls.clear()
print(tracing("t")(retry(3)(flaky))(), calls.count("t.enter"), "次 enter  (tracing 外层)")
```

实际输出：

```
ok 3 次 enter  (retry 外层)
ok 1 次 enter  (tracing 外层)
```

**变化。** 进程内的装饰器链写在代码里，顺序看得见；服务框架里的中间件顺序由配置决定，更容易放错。经验：越是想「无论如何都执行」的（追踪、指标、清理）放越外面；越是依赖请求已被接受的（业务重试）放越里面。

**代价。** 横切逻辑越多，调用栈越深，排查时要在一层层包装里找真正的业务；每个包装层都要保持对异常和返回值透明（不吞异常、不改返回类型），否则外层的行为就被悄悄改变。

**信号。** 多个 handler 里重复同样的鉴权、日志、重试几行。
