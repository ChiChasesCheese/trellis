---
slug: api-circuit-breaker
kind: low-level-design
---
## Q
**熔断器（Circuit Breaker）**｜低层设计

设计一个用于保护外部依赖调用的熔断器：有三种状态（关闭 CLOSED、打开 OPEN、半开 HALF_OPEN），失败阈值、打开持续时间可配置，状态按规则自动转换；线程安全；熔断时可以返回降级（fallback）结果；并暴露指标（成功数、失败数、被拒绝数）以便监控服务可靠性。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 熔断器是一个小状态机：下游持续失败时快速失败、给下游喘息时间，再用少量探测请求判断是否恢复；难点在于状态转换在并发下的正确性（半开期只放少量探测、迟到的旧请求结果不能污染新状态、不持锁调用下游）。

**需求。**
功能：
1. 包装一次下游调用 `call(fn, fallback)`：根据当前状态决定放行或拒绝。
2. 关闭状态：正常放行，连续失败达到阈值就转为打开。
3. 打开状态：直接拒绝（或走降级），不触碰下游；冷却时间到后转为半开。
4. 半开状态：只放行有限的探测请求；探测成功达到要求就回到关闭，任何一次探测失败就立刻回到打开。
5. 提供降级：被拒绝或调用失败时返回降级结果。
6. 暴露指标：成功、失败、拒绝次数和当前状态。

非功能：线程安全；判定开销极小（只持锁做状态判断，不在锁内调用下游）；时间可注入以便测试。

**核心实体与接口。**
- `State`：枚举，三个状态。
- `CircuitOpenError`：拒绝时抛出的异常。
- `CircuitBreaker`：配置（`failure_threshold`、`open_timeout`、`half_open_max_calls`、`success_threshold`、`clock`），内部状态（当前状态、连续失败数、半开成功数、半开在途探测数、打开时刻、状态代号），公开方法 `call(fn, fallback=None)`、属性 `state`、字典 `metrics`。
- 模式：状态模式（State）。三种状态的行为差异不大时，用枚举加条件分支更直接；如果每种状态的行为复杂，则把每个状态做成一个类，转换逻辑放进状态对象。这里选择枚举，因为只有放行判断和结果回报两处分支。降级用策略（回调函数）注入。

```python
from __future__ import annotations

import threading
import time
from enum import Enum
from typing import Callable, TypeVar

T = TypeVar("T")


class State(Enum):
    CLOSED = "closed"        # 正常放行，统计失败
    OPEN = "open"            # 熔断：直接拒绝，不碰下游
    HALF_OPEN = "half_open"  # 试探：只放少量请求，看下游是否恢复


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, open_timeout: float = 30.0,
                 half_open_max_calls: int = 1, success_threshold: int = 1,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.failure_threshold, self.open_timeout = failure_threshold, open_timeout
        self.half_open_max_calls, self.success_threshold = half_open_max_calls, success_threshold
        self._clock, self._lock = clock, threading.Lock()
        self._state, self._failures, self._successes = State.CLOSED, 0, 0
        self._opened_at, self._probes, self._gen = 0.0, 0, 0
        self.metrics = {"success": 0, "failure": 0, "rejected": 0}

    def call(self, fn: Callable[[], T], fallback: Callable[[], T] | None = None) -> T:
        gen = self._try_acquire()                         # 不持锁调用下游：慢调用不能把所有线程锁住
        if gen is None:
            self.metrics["rejected"] += 1                 # 计数器的精确性要求不高；严格时改用原子计数
            if fallback is not None:
                return fallback()
            raise CircuitOpenError("circuit open")
        try:
            result = fn()
        except Exception:
            self._on_result(False, gen)
            if fallback is not None:
                return fallback()
            raise
        self._on_result(True, gen)
        return result

    def _try_acquire(self) -> int | None:
        with self._lock:
            if self._state is State.OPEN:
                if self._clock() - self._opened_at < self.open_timeout:
                    return None
                self._move(State.HALF_OPEN)                                          # 冷却结束，进入试探
            if self._state is State.HALF_OPEN:
                if self._probes >= self.half_open_max_calls:                        # 试探名额已满
                    return None
                self._probes += 1
            return self._gen                                                         # 凭"代号"领取，回报时核对

    def _on_result(self, ok: bool, gen: int) -> None:
        with self._lock:
            self.metrics["success" if ok else "failure"] += 1
            if gen != self._gen:                          # 状态已变：迟到的旧请求结果只计数，不影响新状态
                return
            if self._state is State.HALF_OPEN:
                self._probes -= 1
                if not ok:
                    self._trip()                          # 试探失败：立刻重新熔断，重新计时
                else:
                    self._successes += 1
                    if self._successes >= self.success_threshold:
                        self._move(State.CLOSED)
            elif self._state is State.CLOSED:
                self._failures = 0 if ok else self._failures + 1   # 连续失败计数：一次成功就清零
                if self._failures >= self.failure_threshold:
                    self._trip()

    def _trip(self) -> None:
        self._move(State.OPEN)
        self._opened_at = self._clock()

    def _move(self, new: State) -> None:
        self._state, self._gen = new, self._gen + 1
        self._failures = self._successes = self._probes = 0

    @property
    def state(self) -> State:
        with self._lock:
            return self._state
```

**整体设计。**
`call` 分三步：
1. 取许可 `_try_acquire`：在锁内根据状态判断。打开状态下，冷却时间没到就返回 `None`（拒绝），到了就转入半开；半开状态下，若在途探测数已达 `half_open_max_calls` 就拒绝，否则占一个名额。许可成功时返回当前的"状态代号"（`_gen`）。
2. 调用下游：不持锁。如果在锁内调用下游，一个慢调用会让所有线程排队，熔断器自己变成瓶颈。
3. 回报结果 `_on_result`：在锁内更新状态。关闭状态下，成功清零连续失败数，失败加一，达到阈值则熔断（`_trip`）；半开状态下，失败立刻回到打开并重新计时，成功累计到 `success_threshold` 后回到关闭。

状态转换图：关闭状态连续失败达到阈值，转为打开；打开状态冷却时间到，转为半开；半开状态探测成功，回到关闭；半开状态探测失败，回到打开。

**深入。**

1. 并发正确性的三个陷阱：
- 半开期的"惊群"：冷却一结束，所有等待的线程同时冲向下游，把刚恢复的下游再次打垮。方案：半开只放 `half_open_max_calls` 个探测（通常 1 个），其余继续被拒绝或走降级，探测通过后才全量放行。
- 迟到的旧结果：线程 A 在关闭状态时发出请求，很慢；期间熔断器打开又进入半开；A 的结果此时返回，如果直接计入，会让半开的探测计数错乱（比如把在途数减成负数），或者把一个很久以前的失败当成"探测失败"。方案：每次状态转换让 `_gen` 加一，许可携带领取时的代号，回报时代号不一致就只计入指标、不改变状态。
- 不持锁调用：见上。代价是计数更新与调用不在同一个临界区，所以结果回报时要重新加锁并核对代号。

2. 失败的判定方式：
- 连续失败数（这里的实现）：简单、直观，适合低流量的内部调用；缺点是流量低时一次偶发的成功会清零计数，高流量时少量失败穿插成功永远触发不了熔断。
- 滑动窗口失败率：统计最近 N 次调用（计数窗口）或最近 T 秒（时间窗口）里的失败比例，超过阈值（如 50%）且样本数达到最小值才熔断。更接近生产系统（如 Resilience4j、Hystrix）的做法，实现上要保存窗口内每次调用的结果（环形数组）。
- 慢调用也算失败：调用耗时超过阈值计为失败，防止"不报错但极慢"的下游拖死线程池。
- 哪些异常算失败：业务上的 4xx（参数错误）不应触发熔断，只有超时、5xx、连接失败这类才计入；配置成可传入的异常判定函数。

3. 半开期的策略：
- 探测名额与成功门槛：`half_open_max_calls` 控制同时探测数，`success_threshold` 控制需要连续成功几次才信任下游。名额取 1 最保守，但恢复慢；取多个恢复快，但风险更大。
- 冷却时间：固定值最简单；可用指数退避——每次半开探测失败后把冷却时间翻倍（有上限），下游长时间故障时减少无谓的探测。

4. 降级与可观测：
- 降级要快、不依赖同一个下游：返回缓存的旧值、默认值或空结果。降级本身不应抛出异常，否则熔断的目的落空。
- 指标：成功、失败、拒绝次数，当前状态，状态切换事件（带时间戳）。生产里导出到监控系统，对"进入打开状态"设置告警；拒绝数激增通常比失败数更早反映故障影响面。
- 计数器的更新放在锁外时可能略有误差，监控精度要求不高时可接受；要求严格则统一放进临界区或使用原子计数。

**取舍与追问。**
- 一个下游一个熔断器，还是一个接口一个：粒度太粗，一个坏接口拖垮整个下游的可用性；太细，样本不足、配置繁多。通常按"下游服务加关键接口"划分，并配合舱壁（bulkhead）隔离线程池。
- 与重试、超时的关系：超时是熔断的前提（不超时的慢调用永远不会被计为失败）；重试要放在熔断器外面或配合它，否则熔断打开后重试仍然反复触发。顺序一般是：限流 → 熔断 → 超时 → 重试，具体因框架而异，关键是重试不能绕过熔断。
- 多实例：每个进程各自维护一个熔断器，各自判断，简单且互不依赖；若要集群共享状态，就要引入共享存储，代价是新的故障点，通常不做。
- 线程安全的替代：用 `AtomicReference` 保存不可变状态对象并做 CAS，可以避免锁，适合极高并发；锁版本在多数场景足够，且更易于验证。
- 测试：注入假时钟，验证 关闭到打开、打开到半开、半开到关闭、半开到打开 四条转换；并发测试验证半开期只放行一个探测。

**级别期望。**
- 中级：写出三状态机，失败阈值和冷却时间，能放行、拒绝、恢复。
- 高级：线程安全、不持锁调用下游、半开只放有限探测、降级回调、指标。
- 资深/Staff：状态代号防止迟到结果污染、滑动窗口失败率与慢调用、指数退避冷却、异常分类、与限流重试超时舱壁的组合、分布式部署下的取舍。

**先修概念。** [[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-concurrency-intro|并发入门]]、[[hi-low-level-design-concurrency-correctness|并发正确性]]、[[hi-low-level-design-in-a-hurry-design-principles|设计原则]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]

**同类题。** [[rate-limiter-system|限流器]]、[[solution-thread-pool|线程池]]、[[solution-ttl-cache|带过期的缓存]]、[[multithreaded-logging-framework|多线程日志框架]]
