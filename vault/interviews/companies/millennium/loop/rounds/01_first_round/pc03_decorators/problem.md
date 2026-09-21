# pc03 · Decorators — retry / memoize / timing / rate-limit，从裸装饰器到带参数、带状态

> 45 min 第一轮："Python 内功"分支的代表题：写装饰器不是背语法，是能不能讲清楚"函数在什么时候
> 被调用、`*args/**kwargs` 怎么透传、状态该放在哪一层闭包"。

## 背景

多个独立来源都把"写装饰器"列进 Millennium 第一轮的编码环节：LeetCode Discuss 上一条 Quant
Dev-Python 面经明确写"decorator code writing"是第 5 轮考题；1point3acres 上至少两条独立帖子
（一条标为 Developer OA、一条泛面经列表）单独提到"Python decorator"是考点；聚合站把它和
generator、context manager 归为同一组"Python 内功"题。三个来源没有一个给出完整的题面文字，本题
按"业界最常见的装饰器递进顺序"重建：先写两个最基础的裸装饰器，再写一个带参数的装饰器工厂，最后
写一个带状态的类装饰器——这正好覆盖"装饰器"这个概念在面试里会被问到的三种形态。

## API 契约（英文签名）

```python
def timed(func: Callable) -> Callable: ...
def memoize(func: Callable) -> Callable: ...

def retry(
    times: int,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    backoff: float | Callable[[int], float] = 0,
    sleep: Callable[[float], None] = lambda s: None,
) -> Callable[[Callable], Callable]: ...

def make_flaky(fail_times: int) -> Callable[[], str]: ...

class RateLimitExceeded(Exception): ...

def rate_limited(
    n: int, per_seconds: float, clock: Callable[[], float] = time.monotonic
) -> Callable[[Callable], Callable]: ...
```
`sleep` / `clock` 是可注入的依赖：测试永远不真的 `time.sleep()` 或依赖真实系统时钟，保证结果
确定、跑得快。

## 规则

### Part 1 — `timed` + `memoize`（裸装饰器，一手原题的基础形态）
- `timed(func)`：包装后每次调用把耗时写进 `wrapper.last_seconds`（`time.perf_counter` 计时，
  每次调用都刷新，不是只记第一次）。
- `memoize(func)`：按 `(args, sorted(kwargs.items()))` 做缓存键（要求可哈希）；暴露
  `wrapper.hits` / `wrapper.misses` 两个计数器和 `wrapper.cache_clear()`。
- 两者都必须用 `functools.wraps` 保留被包装函数的 `__name__`、`__doc__`。
- **缓存键是调用形状，不是绑定后的签名**：`f(5)`、`f(5, 0)`、`f(5, b=0)` 即使算出同一个值，
  也是三个不同的缓存条目（因为 `args`/`kwargs` 的原始形状不同）——这是面试里常被追问的"这个
  memoize 实现有什么局限"的切入点。

### Part 2 — `retry(times, exceptions, backoff)`（带参数的装饰器工厂）
- `retry` 本身是一个返回装饰器的函数（"装饰器工厂"），不是装饰器；`times < 1` 在**装饰时**
  （调用 `retry(...)` 的那一刻）就抛 `ValueError`，不等到真正调用包装函数。
- 被包装的调用最多尝试 `times` 次；只有 `exceptions` 元组里列出的异常类型会触发重试，其它异常
  第一次出现就直接向外传播（不重试、不计入 `wrapper.attempts`）。
- 每次失败重试之间调用 `sleep(delay)`；`delay` 是 `backoff(attempt)`（如果 `backoff` 可调用）
  或常数 `backoff`。
- `wrapper.attempts` 记录最近一次调用实际用了几次尝试；耗尽所有尝试后重新抛出**最后一次**捕获
  到的原始异常（类型不变）。
- `make_flaky(fail_times)` 是测试/自检用的辅助函数：返回一个零参函数，自带私有计数器，前
  `fail_times` 次调用抛 `ValueError`，之后每次调用都返回 `"ok"`。

### Part 3 — `rate_limited(n, per_seconds, clock)`（带状态的类装饰器）**(reconstructed)**
- 用类实现装饰器（`__call__`），状态（滑动窗口内的调用时间戳）存在装饰器实例上，不是存在被包装
  函数上。
- 窗口语义：只保留时间戳落在 `(clock() - per_seconds, clock()]` 半开区间内的调用记录，过期的
  惰性淘汰（在下一次调用时才清理，不是用定时器主动清）——和限流器的标准写法一致。
- 窗口内调用数已达 `n` 时，新调用抛 `RateLimitExceeded`，不执行被包装函数。
- `n < 1` 或 `per_seconds <= 0` 在**装饰时**立即抛 `ValueError`。
- `clock` 默认 `time.monotonic`，测试传入可控的假时钟。

## Worked examples（全部由 `solution.py` 实际运行得出）

**Part 1**（`part1(lines)`，line-driven：`MEMO <a> <b>` 用缓存版 `add`；`MEMO CALLS` 打印
`add` 底层实际被调用的次数；`TIMED <x>` 用计时版 `square`）
```python
part1(["MEMO 2 3", "MEMO 2 3", "MEMO 5 1", "MEMO CALLS", "TIMED 4"])
```
→ `["5", "5", "6", "2", "16"]`（`(2,3)` 命中两次缓存但底层只跑一次、`(5,1)` 是新键再跑一次，
所以 `MEMO CALLS` 输出 `2`；`TIMED 4` 输出 `4*4=16`）

**Part 2**（`part2(lines)`，`RETRY <times> <fail_times>`：为每行新建一个 `make_flaky(fail_times)`，
用 `retry(times, exceptions=(ValueError,))` 包装后调用一次）
```python
part2(["RETRY 3 2", "RETRY 3 5"])
```
→ `["ok 3", "error ValueError 3"]`（第一行：`fail_times=2 < times=3`，第 3 次尝试成功，
`attempts=3`；第二行：`fail_times=5 >= times=3`，3 次尝试全部失败，重新抛出最后一次的
`ValueError`，`attempts=3`）

**Part 3**（`part3(lines)`，首行 `LIMIT <n> <per_seconds>`，之后每行 `CALL <t>` 把假时钟拨到 `t`
再调用一次被 `rate_limited(n, per_seconds)` 包装的空操作）
```python
part3(["LIMIT 3 10", "CALL 0", "CALL 1", "CALL 2", "CALL 3", "CALL 11"])
```
→ `["ok", "ok", "ok", "limited", "ok"]`（容量 3：`t=0,1,2` 三次都在窗口内被接受，窗口满；
`t=3` 时窗口 `(3-10,3]=(-7,3]` 里仍有 3 条记录（0,1,2 都满足 `3-0=3<10`），第 4 次被拒绝；
`t=11` 时窗口变成 `(1,11]`，`0` 因为 `11-0=11>=10` 被淘汰，`1` 因为 `11-1=10>=10` 也被淘汰，
只剩 `2`（`11-2=9<10`），窗口里只有 1 条，接受新调用）

## `main()` 命令流

```
PART 1                PART 2              PART 3
MEMO 2 3              RETRY 3 2           LIMIT 3 10
MEMO 2 3              RETRY 3 5           CALL 0
MEMO 5 1                                  CALL 1
MEMO CALLS                                CALL 2
TIMED 4                                   CALL 3
                                           CALL 11
→ 5                   → ok 3              → ok
  5                     error ValueError    ok
  6                     3                   ok
  2                                         limited
  16                                        ok
```

## 边界清单

- Part 1：`memoize` 缓存键区分调用形状——`f(5)` / `f(5, 0)` / `f(5, b=0)` 是三个不同缓存条目
  即使返回值相同；`cache_clear()` 之后计数器归零且下一次调用必须真正重新执行
- Part 1：`timed` 每次调用都刷新 `last_seconds`，不是只在第一次调用时设置
- Part 2：`times < 1` 在装饰时（不是调用时）就抛 `ValueError`
- Part 2：不在 `exceptions` 里的异常类型第一次出现就直接向外传播，`wrapper.attempts` 保持初始
  值 `0`（因为异常发生在 `wrapper.attempts = attempt` 赋值之前），不会触发任何 `sleep`
- Part 2：`backoff` 是可调用时按尝试序号（`1, 2, …`）调用；耗尽后重新抛出的是**最后一次**捕获
  到的异常实例，类型和消息都不变
- Part 3：窗口边界是"**大于等于**"淘汰——`clock() - 最老记录的时间戳 == per_seconds` 时该记录
  被淘汰（半开区间 `(now - per_seconds, now]`），不是"大于"
- Part 3：`n < 1` 或 `per_seconds <= 0` 在装饰时立即抛 `ValueError`
- Part 3：装饰器保留 `__name__`/`__doc__`（`functools.update_wrapper` 用在类实例上而不是普通
  函数上，因为状态存在实例属性里）

## 追问

1. **装饰器什么时候执行？** `@deco` 等价于 `func = deco(func)`，在**模块加载、函数定义那一刻**
   就执行了 `deco(func)` 这次调用（返回 `wrapper`），之后每次"调用被装饰的函数"其实是在调用
   `wrapper`——`retry(...)` 这种"工厂"则多一层：先执行 `retry(times, ...)` 拿到真正的装饰器，
   再执行 `装饰器(func)`。
2. **多个装饰器叠在一起，执行顺序是什么？** `@a`\n`@b`\n`def f(): ...` 等价于
   `f = a(b(f))`：**从下往上包装**（`b` 先包）、**从外往内调用**（调用时先进 `a` 的 wrapper 逻辑，
   再进 `b` 的）——"由内而外定义、由外而内调用"。
3. **为什么 `functools.wraps` 必要？** 不加的话 `wrapper.__name__`/`__doc__` 会变成
   `"wrapper"`/`None`，打日志、生成 API 文档、`inspect` 内省、依赖 `__name__` 做路由/调度的框架
   （比如许多 web 框架按函数名注册路由）都会因此出错；本题的 Part 1 直接用测试验证这一点。
4. **装饰在类方法上，`self` 怎么处理？** 方法本质是"函数 + 隐式第一个参数"，`@memoize` 这类
   装饰器包装的其实是未绑定的函数，`self` 会作为 `args[0]` 出现在缓存键里——如果不同实例应该
   分别缓存，这刚好是正确行为；如果想要"跨实例共享缓存"就需要显式排除 `self`（本题不要求实现，
   属于开放式讨论）。

## 来源与置信度

- **HIGH** LeetCode Discuss 7423863（Quant Dev-Python 面经，第 5 轮）："decorator code writing"。
- **HIGH** 1point3acres thread-1079245（Developer OA 面经）与 thread-1143768：均提到 Python
  decorator 是考察点之一。
- **MED** 聚合站（TechPrep / InterviewQuery）把 "decorators, generators, context managers" 列为
  同一组 Python 内功考点，未标出具体轮次。
- `../../catalog/raw/coding_first_round.md`（若尚未落盘，以本文件所属的
  `tasks/AGENT_PROBLEMS.md` §2 pc03 行为准）。
- 以上来源均只给出"考装饰器"这一事实，没有给出完整题面；三个 Part 的具体规则、API 形状与全部
  worked examples 均为 **(reconstructed)**，按"裸装饰器 → 带参数装饰器 → 带状态类装饰器"这条
  业界最常见的装饰器递进结构设计。

## 考什么

S03 Python 内功（闭包、`*args/**kwargs` 透传、`functools.wraps`）· S07 依赖注入做可测试的时间/
时钟（`sleep`/`clock` 参数化，不真的睡眠或依赖系统时钟）· 装饰器三种形态：裸装饰器 → 参数化的
装饰器工厂 → 带状态的类装饰器。
