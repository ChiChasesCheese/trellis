# pc03 Decorators — report

## Summary
三个独立来源都把"写装饰器"列进 Millennium 第一轮编码考点（LeetCode Discuss Quant Dev-Python
面经第 5 轮明确写 "decorator code writing"；两条 1point3acres 帖子独立提到 Python decorator），
但都没有给出完整题面。3-part 按"裸装饰器 → 带参数的装饰器工厂 → 带状态的类装饰器"这条业界最
常见的递进结构重建：Part 1 `timed`/`memoize` → Part 2 `retry(times, exceptions, backoff)` →
Part 3 `rate_limited(n, per_seconds, clock)` **(reconstructed)**。

## Sources & confidence
HIGH（LeetCode Discuss 7423863 Round 5、1point3acres thread-1079245 / thread-1143768，三个来源
独立确认"考装饰器"这一事实）；三个 Part 的具体规则、API 形状、worked examples 均为重建。

## Approach by part
1. `timed`/`memoize` 是标准的裸装饰器：`functools.wraps` 保留元数据；`memoize` 的缓存键是
   `(args, sorted(kwargs.items()))` 的原始调用形状，不做参数绑定归一化（这个局限本身就是追问
   素材）；`hits`/`misses`/`cache_clear` 挂在 `wrapper` 上做可测试的内省点。
2. `retry` 是装饰器工厂：先校验 `times >= 1`（装饰时就失败，不拖到调用时），再返回真正的
   `decorator(func) -> wrapper`；`wrapper` 内部一个 `for attempt in range(1, times+1)` 循环，
   `except exceptions` 精确捕获，未匹配类型的异常直接从 `func()` 那行原样传播，不经过任何
   `wrapper.attempts` 赋值。`make_flaky` 用一个闭包里的私有计数器模拟"调用几次后才成功"。
3. `rate_limited` 用类（`__call__`）实现，状态（`deque` 时间戳队列）挂在装饰器**实例**上而不是
   模块级/函数级，`functools.update_wrapper(self, func)` 把元数据拷到实例上；淘汰逻辑是"下一次
   调用时才清理过期时间戳"的惰性淘汰，和 `rate_limited` 常见的限流器实现同一个写法。

## Pitfalls hidden tests target
- `memoize` 缓存键区分调用形状：`f(5)` / `f(5, 0)` / `f(5, b=0)` 是三个不同缓存条目（即使值
  相同），只有完全相同的调用形状才命中缓存
- `timed` 每次调用都刷新 `last_seconds`，不是只在首次调用时赋值一次
- `retry(0)` / `retry(-1)` 在**装饰时**立即抛 `ValueError`，不需要真正调用包装函数就能触发
- 不在 `exceptions` 元组里的异常类型第一次出现就直接传播，`wrapper.attempts` 停在初始值 `0`
  （因为赋值语句在 `func()` 调用之后，异常从调用处直接跳出，赋值根本没执行到）
- `backoff` 作为可调用对象时按尝试序号（1, 2, …）调用，成功的最后一次尝试之后不再 `sleep`
- `rate_limited` 窗口边界是"age >= per_seconds 才淘汰"（半开区间 `(now-per_seconds, now]`），
  边界值 `age == per_seconds` 必须被淘汰而不是保留
- `rate_limited(0, ...)` / `rate_limited(..., 0)` / 负数 `per_seconds` 在装饰时抛 `ValueError`
- 大量重复调用下的性能：20 万次 `retry`-包装调用、20 万次 `rate_limited`-包装调用均需在预算
  时间内完成，且 `rate_limited` 的接受/拒绝计数必须和滑动窗口的理论值吻合

## Complexity & measured cost
`timed`/`memoize` 单次调用 O(1)（哈希查找）；`retry` 单次调用 O(times)；`rate_limited` 单次调用
均摊 O(1)（惰性淘汰，每个时间戳最多被淘汰一次）。编排者验证：20 万次 `retry(3)` 包装的恒成功调用
0.07 s；20 万次 `rate_limited(1000, 1.0)` 包装调用（模拟时钟均匀推进 2 秒）0.21 s，接受计数精确
等于理论值 2000（= 1000 次/秒 × 2 秒）；两者都远低于 2 s 预算。

## Test inventory
21 test functions（`grep -c "def test"` = 21，无参数化展开，pytest 收集数与函数数一致）——
`uv run --project /home/user/trellis --with pytest python -m pytest loop/rounds/01_first_round/pc03_* -p no:cacheprovider` → `21 passed`；
`IMPL=starter` 同一条命令 → `17 failed, 4 passed`（4 个通过是因为 starter 的裸桩装饰器等价于
"什么都不做直接返回原函数"，元数据保留、异常直传、恒成功场景下的性能测试在这种空实现上本就会
通过，属于弱测试的已知边界，不影响"大面积红"的验收口径）。按 marker 统计（`grep -oE`）：
part1 7 · part2 8 · part3 6；edge 10 · fmt 1 · perf 2 · io 3。

## Skills exercised
S03 Python 内功（闭包、`*args/**kwargs` 透传、`functools.wraps`）· S07 依赖注入做可测试的时间/
时钟（`sleep`/`clock` 参数化）· 装饰器的三种形态：裸装饰器、参数化装饰器工厂、带状态的类装饰器。
