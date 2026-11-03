# 熔断器（Circuit Breaker）

服务要调用一个不太稳定的下游。下游持续出错时，继续调用只会拖垮自己的线程池，也让下游没有机会恢复。
熔断器包在调用外面：连续出错就"跳闸"，之后的调用直接被拒绝或走降级；过一会儿放少量探测过去，下游恢复了再放行。
照机考的节奏分关来做，做完一关再看下一关。

**分关要求**

- 第 1 关（约 20 分钟）：三个状态（`CLOSED` / `OPEN` / `HALF_OPEN`）和四条转换：关闭时连续失败达到阈值就打开；
  打开时拒绝调用，冷却时间到后下一次调用转入半开；半开时那一次探测成功就关闭、失败就重新打开并重新计时。
  被拒绝或下游失败时可以走降级函数；暴露成功、失败、被拒绝的计数。时间可注入。
- 第 2 关（约 20 分钟）：并发正确性。半开期最多同时放行 `half_open_max_calls` 个探测，其余继续被拒绝；
  `success_threshold` 次探测成功才关闭；调用下游时不能持有锁；迟到的旧请求结果不能改变新状态（只计数）；
  多线程下计数必须精确。
- 第 3 关（约 15 分钟）：失败的判定。`is_failure` 决定哪些异常算下游失败（比如业务 4xx 不算）；
  可选的滑动窗口失败率代替连续失败数；耗时过长的调用也算失败。
- 第 4 关（选做）：每次探测失败后冷却时间翻倍（有上限），恢复后复位；状态变化通知 `on_state_change`，
  在锁之外调用，回调出错不影响熔断器。

**接口**

```python
class State(Enum): CLOSED; OPEN; HALF_OPEN
class CircuitOpenError(Exception)                                  # 被拒绝且没有降级函数
@dataclass(frozen=True, slots=True) class Metrics: success: int; failure: int; rejected: int

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, open_timeout: float = 30.0,
                 half_open_max_calls: int = 1, success_threshold: int = 1,
                 clock: Callable[[], float] = time.monotonic, *,
                 is_failure: Callable[[Exception], bool] = lambda exc: True,
                 window_size: int | None = None, min_calls: int = 10, failure_rate: float = 0.5,
                 slow_call_threshold: float | None = None,
                 backoff_factor: float = 1.0, max_open_timeout: float = 300.0,
                 on_state_change: Callable[[State, State], None] | None = None) -> None
    def call(self, fn: Callable[[], T], fallback: Callable[[], T] | None = None) -> T
    @property state -> State
    @property metrics -> Metrics
```

规则细节：

- 配置不合法抛 `ValueError`：`failure_threshold`、`half_open_max_calls`、`success_threshold` 小于 1，`open_timeout` 小于 0，`backoff_factor` 小于 1，
  `failure_rate` 不在 (0, 1]，设了 `window_size` 时 `min_calls` 不在 [1, window_size]。
- 冷却判定：`clock() - 打开时刻 >= open_timeout` 即结束（恰好等于也算）。状态不会自己随时间变化：`state` 在 OPEN 过了冷却时间后仍是 `OPEN`，要等下一次 `call` 才转入半开。
- `call` 被拒绝：有 `fallback` 返回它的结果，否则抛 `CircuitOpenError`，不调用 `fn`，`rejected` 加一。
- `fn` 抛 `Exception`：若 `is_failure(exc)` 为真，记一次失败，有 `fallback` 返回它的结果，否则原样抛出；为假则记一次成功并原样抛出（降级不掩盖这类答复）。`KeyboardInterrupt` 等非 `Exception` 直接穿过，不计数。
- 半开期成功计数和在途探测数在每次状态转换时清零。窗口模式下（`window_size` 不为空）不再看连续失败数：最近 `window_size` 次里至少 `min_calls` 次且失败比例 `>= failure_rate` 才打开，窗口在状态转换时清空。
- `slow_call_threshold`：`clock()` 测得的耗时 `>=` 阈值就算失败，但调用方照样拿到返回值。
- 指标：迟到的旧请求结果只计入指标，不改变状态。

例子：

```python
now = [0.0]
cb = CircuitBreaker(failure_threshold=2, open_timeout=10, clock=lambda: now[0])
# 两次 cb.call(boom) 都抛出 boom 的异常 -> cb.state is State.OPEN
cb.call(boom, fallback=lambda: "cached")   # "cached"，没碰下游，metrics.rejected == 1
now[0] = 10
cb.call(lambda: "ok")                      # "ok"：冷却结束，这次调用是探测，成功后 cb.state is State.CLOSED
cb.call(boom)                              # 不会抛 CircuitOpenError，抛的是 boom 自己的异常
```

**评分点**

- 状态机清楚：四条转换写得出，非法转换在代码里有守卫；能说出为什么用枚举加条件分支，而不是每个状态一个类。
- 拿许可、调用下游、回报结果是三步：下游调用不持锁；能说清持锁调用的后果。
- 半开期限流探测，避免冷却结束时惊群；名额和成功计数的含义分得清。
- 迟到的旧结果：用代号（generation）核对，转换时让代号加一；能举出不加代号会出错的具体时序。
- 失败判定可配置：业务错误不算下游故障；滑动窗口解决"低流量、失败穿插成功"的问题；慢调用也要算。
- 指标精确（计数在锁内更新），指标快照不可变；降级函数本身不应抛异常。
- 回调在锁外调用；回调出错不影响熔断器；时间可注入，测试里没有 `sleep`。
- 能口述：与超时、重试、限流、舱壁的顺序关系；一个下游一个熔断器还是一个接口一个；多实例是否共享状态。
