# bs05 · fetchrace：Semaphore 异常路径不归还 + gather 异常被算成成功，练"为什么 asyncio 的并发 bug 反而更好复现"

> [!tldr]
> - 这轮考的不是"你会不会写 `asyncio`"，是能不能看出一个"每次都必现的死锁"和一个"数值算错但
>   不崩溃"的 bug 各自该往哪个方向查
> - 三步套路：先分清"这是超时/死锁类还是错值类" → 死锁类去数"每一次 `acquire()` 有没有对应的
>   `release()`，哪怕在异常路径上" → 错值类去看 `isinstance` 检查是不是写在了副作用之后
> - 最值得带走的一个信号：**`asyncio` 是单线程协作式调度，同样的输入产生同样的交错**——这意味着
>   `asyncio` 版本的并发 bug 通常不需要 `Barrier` 也能"每次跑都必现"，这跟 `threading` 版本
>   （见 `bs04`）的调试体验完全不同

## 1. 题目在说什么
`fetchrace` 用 `asyncio` 并发抓取一串 URL，用一个 `Semaphore` 限制同时在飞的请求数，每个 URL
失败会指数退避重试，最后把"成功或失败"的结果汇总成一份 `Stats`——一个 URL 失败不应该拖累其他
URL，也不应该让整个任务崩掉。两条 issue：

```
Bug report 1 — 低并发下，失败的 URL 够多，fetch_all() 会永远卡住
> concurrency=2，前两个 URL 都失败，第三、第四个 URL 永远等不到轮到自己——
> 用完全相同的 4 个 URL 和 concurrency=2，每次跑都会卡住，不是偶尔。

Bug report 2 — 失败的请求在最终 Stats 里被算成了成功
> aggregate() 直接传一个真实结果 + 一个异常进去，期望 succeeded=1, failed=1，
> 实际 succeeded=2, failed=0。
```

Bug 1 是"资源没归还"（死锁），Bug 2 是"该判断类型但没判断"（逻辑错误）——两者都不是靠运气才
复现，这是这轮题目专门设计的地方。

## 2. 读库：3 分钟摸清结构
1. **README 的 Layout**：`http_client.py`（一次 GET，跑在线程池里）→ `retry.py`（指数退避
   重试）→ `crawler.py`（`fetch_one` 拿信号量名额 → `fetch_all` 建任务丢给 `gather` →
   `aggregate` 把结果列表翻译成 `Stats`）。
2. **一次抓取的路径**：`fetch_all` 给每个 URL 建一个 `fetch_one` 任务，交给
   `asyncio.gather(*tasks, return_exceptions=True)`——`return_exceptions=True` 意味着某个任务
   内部抛异常不会中断 `gather`，异常对象会原封不动地出现在结果列表里对应的位置上。
3. **跑测试**：`python -m pytest tests -q`，12 个测试，2 红，都在 `test_crawler.py`。

## 3. 下手顺序（面试里就按这个来）
1. **先分清这条失败是"超时/卡住"还是"值算错"**：
   `test_fetch_all_does_not_deadlock_when_some_urls_fail_under_low_concurrency` 用
   `asyncio.wait_for(..., timeout=0.5)` 包住了调用——这是故意设计成"卡住时快速报错，而不是真的
   挂起测试进程"，读到 `TimeoutError`/`CancelledError` 就说明是死锁类。
   `test_aggregate_separates_exceptions_from_successes` 报的是 `assert 3 == 2`——这是值算错，
   跟并发完全无关（这条测试甚至不启动任何 `asyncio` 事件循环，直接传一个手造的 list 给
   `aggregate`）。
2. **死锁类：数"acquire 有没有对应的 release，包括异常路径"**：`Semaphore` 的语义是"每次
   `acquire()` 必须最终对应恰好一次 `release()`，不管中间正常跑完还是半路抛异常"。读
   `fetch_one`：`await sem.acquire()` 之后调用 `fetcher(url)`，再 `sem.release()`——如果
   `fetcher(url)` 抛异常，`release()` 这一行根本不会被执行到。
3. **错值类：看类型判断写在副作用之前还是之后**：读 `aggregate` 的循环体，`stats.succeeded += 1`
   是不是在 `isinstance(item, Exception)` 判断**之前**无条件执行的。
4. **假设，然后验证**：死锁类的验证很直接——数一下 4 个 URL、`concurrency=2`、前两个失败，够
   耗尽 2 个名额且永远不释放，第三、四个自然永远拿不到名额；不需要额外打印，逻辑本身就能推出
   死锁必现。错值类同理，读一遍循环体的执行顺序就能确认。
5. **最小修复 + 回归**：死锁类改成 `try/finally`；错值类把"先分类、再各自加一次"改对。改完
   `pytest tests -q` 全部 12 个应该都过。

## 4. 调试工具怎么用
`asyncio` 代码调试的关键是"先分清超时类还是错值类"，pdb 命令表见
`loop/rounds/04_bug_squash/DEBUG_101.md`，这里只说这道题具体怎么用——

- 死锁类（超时）：`asyncio.wait_for(coro, timeout=0.5)` 本身就是"注入让出点、快速失败"的写法，
  遇到别人写的并发测试如果卡住不动，先看有没有类似的超时包装，没有就自己临时加一个，避免测试
  真的挂起卡住整个调试会话。
- 想看清楚 Semaphore 计数器实时的值，可以在 `fetch_one` 里打印
  `f"acquire url={url} value={sem._value}"`（`_value` 是内部实现细节，仅用于临时调试，不要
  写进正式代码）——比断点更适合看"名额消耗到第几个 URL 就不够用了"。
- 验证 bug 2 完全不需要起事件循环：直接在一个普通同步测试/REPL 里 `aggregate([FetchResult(...),
  RuntimeError(...)])`，比套一层 `asyncio.run` 更快定位到问题跟并发无关。

## 5. 本题两个 bug 的排查实录

**Bug 1 — `sem.release()` 没写在 `finally` 里（Semaphore 许可泄漏 → 死锁）**
- 现象：`test_fetch_all_does_not_deadlock_when_some_urls_fail_under_low_concurrency` 抛
  `TimeoutError`（从 `asyncio.wait_for` 包装出来，链式关联到 `sem.acquire()` 内部的
  `CancelledError`）。
- 定位路径：读测试的 docstring，先理解"为什么这个死锁是必现的，不是偶尔"——`asyncio` 单线程
  协作式调度，同一组 URL、同样谁失败谁成功，交错方式是完全确定的，不需要 `Barrier` 就能保证
  每次跑出一样的结果。读 `fetch_one`：`await sem.acquire()` → `await fetcher(url)` →
  `sem.release()`（作为普通语句，写在调用之后）。`fetcher` 抛异常时，`release()` 这一行永远
  不会执行——名额永久少了一个。`concurrency=2`，前两个 URL 都失败，两个名额都被永久吃掉，第三、
  四个 URL 在 `await sem.acquire()` 上永远等不到。
- 根因分类：**资源没有在异常路径上归还**——`acquire`/`release` 是一对必须成对出现的操作，
  正常路径写对了，异常路径漏了。
- 修复：把 `fetcher(url)` 调用和 `release()` 包进 `try/finally`，让 `release()` 无论正常返回
  还是抛异常都会执行。

**Bug 2 — `aggregate` 先无条件加成功计数，再判断类型（逻辑错误）**
- 现象：`test_aggregate_separates_exceptions_from_successes` 传入一个正常结果 + 一个异常，
  期望 `succeeded=1, failed=1`，实际 `succeeded=2, failed=0`。
- 定位路径：这条测试完全绕开了 `asyncio`，先确认它跟 bug 1 无关（不同的函数，不同的调用方式）。
  读 `aggregate` 的循环体：`stats.succeeded += 1` 写在最前面、对每一项都无条件执行，
  `isinstance(item, Exception)` 的判断在它后面才做，只用来决定要不要额外 append 到
  `stats.errors`——`stats.failed` 这个字段在整个函数里从来没被赋值过，是个死字段。
- 根因分类：**逻辑错误**（分支顺序反了：应该先判断类型再决定加哪个计数器，写成了先加计数器
  再判断类型）。
- 修复：把 `succeeded`/`failed` 的自增分别放进 `isinstance` 判断的两个分支里，保证每一项只
  命中其中一个。

**一个可迁移的信号**：`asyncio` 的并发 bug 里，"每次跑都必现的卡住/超时" → 先怀疑某个
`acquire`/`lock`/连接池 checkout 的归还写在了正常路径的最后一行、没有用 `try/finally`；
"结果列表里混着正常值和异常对象，统计数字对不上" → 先怀疑处理这个列表的代码有没有真的用
`isinstance` 区分两种元素，还是想当然地把它们当成同一种东西处理。

## 6. 面试里怎么说
- 看到 `asyncio.wait_for(..., timeout=...)` 先说明白它的作用：「这是让死锁'快速失败'而不是真的
  卡住测试进程的写法，我不会去改这个超时时间来让测试'过'。」
- 讲 bug 1 时点出不变量：「`Semaphore` 的规则是每次 `acquire` 都要有恰好一次 `release`，不管
  走的是正常路径还是异常路径——我把归还这一步放进 `finally`，这样不管 `fetcher` 是正常返回还是
  抛异常，名额都会还回去。」
- 讲 bug 2 时说明为什么先单独测 `aggregate`：「这个函数是纯逻辑，不涉及任何 `asyncio`，我可以
  直接传一个手造的列表进去，把它和并发那个 bug 完全隔离开测。」
- 交付时说明验证范围：「两个改动一个是 `try/finally`，一个是把计数器挪到判断分支里；我确认了
  全部 12 个测试都过，两个 bug 互不影响对方的修复。」

## 7. 常见跑偏
- **调大测试里的 `concurrency` 来"绕过"死锁**：这样这条具体的测试可能不再卡住，但没有修到真正
  的问题（`release` 没在异常路径上执行）——只要失败的 URL 数量够多，任何并发上限都会重新卡住。
- **把 `aggregate` 改成只认这条测试用的具体异常类型**：让这一个用例过，但对其他任何异常类型都
  不成立——应该用通用的 `isinstance(item, Exception)`，不是针对某个具体异常消息做特判。
- **把 `return_exceptions=True` 改成 `False` 来"解决"死锁**：这会让第一个失败的任务直接取消
  掉其他所有任务，改变了"一个 URL 失败不该影响其他 URL"这个题面明确要求的行为，是绕开问题而不是
  修复它。

## 8. 真实库对应 + 延伸练习
这两个 bug 都是极常见的真实模式："信号量/连接池的归还写在异常路径覆盖不到的地方"（连接池
checkout/checkin、锁的 acquire/release 都属于这一大类）和"`gather(return_exceptions=True)`
返回的列表里，异常对象被当成普通结果处理，没有做类型区分"——两者都是 async Python 代码里反复
出现的 bug 类别，不针对某一个具体上游 issue。

跟 `bs04`（`threading`）对比着看会更清楚一个共同规律：**`asyncio` 单线程协作式调度，交错方式
由输入完全决定，所以并发 bug 反而更容易写成"每次跑都必现"的测试**（这道题两个 bug 都不需要
`Barrier`）；`threading` 是真正的多线程，交错方式受操作系统调度影响，需要 `Barrier`/足够长的
`sleep` 主动撑大竞态窗口才能让 bug 稳定复现（见 `bs04`）。识别"这是 `asyncio` 还是
`threading`"，直接决定了要不要在测试里找同步原语来强制交错。

延伸练习：`python3 loop/mock.py start bs05` → `test` → `ref`。第二遍练习时，试着自己把
`fetch_one` 改回 bug 版本，再手写一条最小 repro（不用测试框架，直接 `asyncio.run`），确认自己
不看 `README.md` 也能从"卡住不动"这个现象推出"某个 `acquire` 没有对应的 `release`"这个假设。
