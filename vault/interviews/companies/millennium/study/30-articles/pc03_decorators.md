# pc03 · 装饰器：裸装饰器 → 带参数的工厂 → 带状态的类

> [!tldr]
> - 这题考的是：`@deco` 到底在什么时候执行、状态该存在闭包/工厂/实例里的哪一层
> - 三步套路：裸装饰器（`functools.wraps` 保元数据） → 参数化装饰器工厂（多一层函数） →
>   带状态的类装饰器（状态挂在实例上）
> - 最值得带走的一个模式：可测试性靠"注入"——真实时钟/真实 `sleep` 换成参数 `clock`/`sleep`，
>   测试永远不真的等、不依赖系统时间

## 1. 题目在说什么（人话版）
写四个装饰器，一个比一个"重"：`@timed` 记录函数跑了多久；`@memoize` 记住算过的结果、别重复算；
`@retry(3)` 失败了自动重试几次；`@rate_limited(3, per_seconds=10)` 限制某个函数 10 秒内最多被调
3 次。前两个装饰器"裸用"（`@timed` 后面不跟括号），后两个要传参数（`@retry(times=3)`），最后一
个还要**记住状态**（"最近调用过几次、什么时候调的"）。

## 2. 读题：把文字变成模型
- **实体**：被装饰的函数、装饰器本身、装饰器需要的额外参数（`times`、`n`、`per_seconds`）。
- **输入长什么样**：一个普通 Python 函数（任意签名），加一层或几层 `@`。
- **输出要什么**：一个行为增强过的函数，调用方式和原函数完全一样（`*args, **kwargs` 原样透传），
  但额外有 `__name__`/`__doc__` 不能丢、可能还挂了 `wrapper.hits`/`wrapper.attempts` 这类内省
  属性。
- **状态**：`memoize` 的缓存、`retry` 的重试计数、`rate_limited` 的调用时间戳——分别应该放在
  哪里？这决定了用简单闭包变量，还是要升级成类。
- **一句话建模**：这是一道**"函数是一等公民，闭包就是对象"**的题——裸装饰器练"函数包函数"，
  参数化装饰器练"再包一层"，类装饰器练"状态该挂在谁身上"。

> [!note] 为什么 `retry` 要比 `timed` 多一层函数
> `@timed` 直接写成 `def timed(func): def wrapper(*a,**k): ...; return wrapper`，`@` 语法糖
> 等价于 `func = timed(func)`，一步到位。但 `@retry(times=3)` 需要先把 `times=3` 传进去、再拿到
> 一个"真正的装饰器"去包 `func`——所以要多包一层：`retry(times) -> decorator(func) -> wrapper`。
> 一句话记忆："`@xxx` 后面有没有括号，就是'裸装饰器'和'装饰器工厂'的区别。"

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：先写 `timed(func)` 的三行结构（记录开始时间 → 调用 → 记录耗时），用
   `functools.wraps` 包一下，立刻手测一次调用。
2. **Part 1 最小可用**：`memoize` 照着 `timed` 的骨架改——把"记时间"换成"查缓存字典、没有就算
   并存起来"，`hits`/`misses` 两个计数器是免费的调试信息，顺手加。
3. **Part 2 叠加**：`retry` 先写外层 `def retry(times, ...): if times < 1: raise ValueError(...)`
   （装饰时就校验，别拖到调用时），再写 `def decorator(func): def wrapper(*a,**k): for attempt
   in range(1, times+1): try: ... except exceptions: ...`。**先写"重试次数用尽后怎么办"**（重新
   抛出最后一次异常），再补 `sleep`/`backoff`，最后处理"不匹配的异常类型不重试"。
4. **收尾（Part 3）**：`rate_limited` 从"函数嵌套函数"换成"类实现 `__call__`"——状态（时间戳
   队列）是实例属性，不是闭包变量；`functools.update_wrapper(self, func)` 是类版本的
   `functools.wraps`。滑动窗口的淘汰逻辑直接照抄"限流器"的标准写法：`while queue and now -
   queue[0] >= window: queue.popleft()`。

## 4. 代码怎么组织
```
timed(func) -> wrapper                    # 裸装饰器：记时间
memoize(func) -> wrapper                  # 裸装饰器：缓存字典 + hits/misses
retry(times, exceptions, backoff, sleep)  # 装饰器工厂：先校验参数
  -> decorator(func) -> wrapper           #   再包函数：try/except 循环 + attempts 计数
make_flaky(fail_times) -> flaky           # 测试用：自带计数器的"前 N 次失败"函数
class RateLimitExceeded(Exception)
rate_limited(n, per_seconds, clock)       # 装饰器工厂
  -> decorator(func) -> _RateLimiter(func) instance   # 类装饰器：状态挂实例
main(stdin, stdout)                       # 按 PART 分发
```
注意 `retry`/`rate_limited` 都是"工厂返回装饰器"，参数校验放在工厂这一层（装饰时报错），不要
下沉到 `wrapper` 里（调用时才报错）——面试官很容易用"什么时候报错"这个问题检验你是否真的理解
`@retry(times=0)` 这行代码本身就已经在调用 `retry(0)` 了。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
def retry(times, exceptions=(Exception,), backoff=0, sleep=lambda s: None):
    if times < 1:
        raise ValueError("times must be >= 1")     # 装饰时就报错，不等调用
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, times + 1):
                try:
                    result = func(*args, **kwargs)
                    wrapper.attempts = attempt
                    return result
                except exceptions as exc:            # 只重试指定类型，其它类型直接冒泡
                    last_exc = exc
                    wrapper.attempts = attempt
                    if attempt < times:
                        sleep(backoff(attempt) if callable(backoff) else backoff)
            raise last_exc                            # 用尽尝试次数：重新抛出最后一次异常
        wrapper.attempts = 0
        return wrapper
    return decorator
```

## 6. 面试里怎么说（边写边讲）
- 开始前："Just to confirm: `@retry(times=3)` means up to 3 attempts total, and I should inject
  `sleep` so tests don't actually wait — is that the right shape?"
- 写 Part 2 时："I'm validating `times >= 1` at decoration time, not call time, since that's a
  configuration error the caller should see immediately."
- 交付时："All three decorators preserve `__name__`/`__doc__` via `functools.wraps`; if time
  allows I'd add a max-backoff cap to `retry` for production use."

## 7. 常见跑偏（方法层面，3 条）
- 忘了 `functools.wraps`，装饰完的函数 `__name__` 变成 `"wrapper"`——面试官一问"这个函数叫什么
  名字"就露馅。
- `retry` 的参数校验和重试循环写反了位置：`times < 1` 的检查放进了 `wrapper` 里，导致
  `@retry(times=0)` 这行代码本身不报错，等真正调用时才报错——面试官会追问"这个错误应该在哪一步
  被发现"。
- `rate_limited` 的时间戳队列直接存成模块级全局变量或闭包里的可变默认参数，导致所有被装饰的
  函数共享同一个窗口——应该在**每次装饰一个新函数**时创建一个新的队列实例。

## 8. 同族题 / 延伸
- `../../snowflake/loop/rounds/03_phone_coding/pc03_recent_event_stream/`：同一个"惰性淘汰、
  在下一次操作时才清理过期记录"的滑动窗口写法，用在事件流而不是限流器上。
- 本 kit `pc04_big_integer_strings/`：同一轮的另一道"Python 内功"题，风格互补（一个考函数式
  编程，一个考手写数值运算）。
- 练习命令：`python3 loop/mock.py start pc03`
