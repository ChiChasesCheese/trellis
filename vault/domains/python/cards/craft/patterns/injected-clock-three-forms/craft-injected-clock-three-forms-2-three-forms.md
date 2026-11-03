---
id: craft-injected-clock-three-forms-2-three-forms
node: craft.patterns.injected-clock-three-forms
type: qa
step: 2
---
## Q
**注入时钟 · 三种形态各自适合什么**｜模式

限流器、KV 存储、电梯模拟都要「让时间可控」，但三者的做法不一样：一个构造时传时钟，一个让每个方法收时间戳，一个干脆没有时钟、只有 `step()`。它们是同一个想法吗？该怎么选？

## A
**要点。** 同一个目的：时间是输入，不是环境。三种形态的差别在于「时间由谁推进、推进几个对象」。

```python
# ① 构造注入 Clock（rate-limiter）：对象自己读，测试给它假时钟
def __init__(self, factory, *, clock: Clock = time.monotonic, ...)

# ② 时间戳作方法参数（kv-store）：类里根本没有时钟
def set(self, timestamp: int, key: str, field: str, value: str, ttl=None)

# ③ 离散 tick（elevator）：一次 step 走一格，没有 sleep
def step(self) -> CarEvent | None:
    """推进一个 tick：开着门就数门的计时，否则按策略走一格或者开门。"""
```

选择：①适合有后台逻辑、调用方不关心时间的服务；②适合「每个操作都带时间戳」的接口（调用方本来就给出事件发生的时间）；③适合多个对象要同步推进的模拟（电梯、机器人），一个 tick 只做一件事，每一步都可以单独断言。

**不变。** 业务逻辑里没有 `time.sleep`，也没有直接读系统时钟。**变化。** ① 的时间是拉（对象问时钟），② 是推（调用方告诉对象），③ 是离散的。

**见于。** rate-limiter、ttl-cache、kv-store、bank-account、amz-occupancy-tracker、elevator、task-scheduler、amz-robot-restaurant。

**信号。** 需求里出现「过期」「冷却」「N 秒内」「定时」；或者你想在测试里写 `time.sleep`。
