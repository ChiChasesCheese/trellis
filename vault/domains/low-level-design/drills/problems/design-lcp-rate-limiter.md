---
nodes: [lcproject.lcp-rate-limiter, concurrency-depth.compound-actions, data.defensive-copy]
tags: [problem]
---
# Drill：LLM 网关限流器（Rate Limiter）

一个 LLM API 网关在接收每个请求之前，调用进程内的限流器：放行还是拒绝，还剩多少额度，多久之后有额度恢复。
限流器支持滑动窗口和令牌桶两种策略，按客户端与接口分别计数，被多个线程同时调用，并提供一个统计接口。
计划用时 45 分钟，最后留出时间写两篇关于锁和多实例的短文。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先读合同，把 `starter.py` 文档字符串里的十二条规则逐条用自己的话改写成断言。
  然后只做滑动窗口：窗口 10000 ms、`limit=2`，在 0、3000、3500 ms 的返回值必须是 `(True,1,10000)`、`(True,0,7000)`、`(False,0,6500)`。
  时钟从构造函数注入，整套测试里不许出现 `sleep`。
- 第 2 关（约 15 分钟）：令牌桶。小数令牌数，用到时才补；`capacity=3`、`refill_rate=0.5`，桶空后过 1200 ms 应得 `(False,0,800)`。
  毫秒数向 0 截断，类型是 `int`；被拒的请求不写任何状态。
- 第 3 关（约 10 分钟）：`(client_id, endpoint)` 隔离，`stats()` 的四个字段，非法参数在动状态之前抛 `ValueError`。
- 第 4 关（约 10 分钟）：两百个线程用屏障抢五十个额度，放行数恰好 50；让一次决策与它的计数更新在同一把锁里；
  闲置 key 的状态可回收，且回收不改变任何判定。选做：`cost`，按接口配不同限额。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-rate-limiter/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-rate-limiter -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把十二条规则和三个数字例子交给它，
一次只给它一个失败的测试，让它先写策略 A，再写策略 B。锁的范围、`remaining` 的口径、时间的表示、被拒是否留痕这些设计决定自己留着，
写在给它的指令里。每次改动之后先跑全部测试，再读 diff：它有没有改测试、有没有改公开签名、锁里有没有多出或少了步骤。
最后自己写那五个最要紧的测试，不要让它代写。

**评分点**
- 开工前把合同定成规则：`remaining` 在决策之后算、被拒为 0、毫秒向 0 截断、被拒不留痕、按 key 隔离（[[lcp-rate-limiter-contract-rules]]）。
- 说得出每个 key 的状态、只在放行时写的不变量，读时钟在锁内（[[lcp-rate-limiter-state-and-invariant]]）。
- 给编程智能体的第一条指令带着合同和数字例子，拆小步，自己留着锁的范围等决定（[[lcp-rate-limiter-first-instruction-to-agent]]）。
- 用同一把锁罩住读时钟、判定、记账、计数，说清 GIL 为什么不够、代价与分片（[[lcp-rate-limiter-race-check-then-count]]）。
- 被拒的请求不延长锁定：重试风暴下 t=100 仍然放行（[[lcp-rate-limiter-retried-rejection]]）。
- 整数纳秒代替浮点秒，窗口边界左闭右开，注入时钟（[[lcp-rate-limiter-boundary-and-truncation]]）。
- 令牌数保留小数，被拒时算对 800 ms，`refill_rate=0` 不除零（[[lcp-rate-limiter-fractional-tokens]]）。
- 能在智能体写出的判定里找出四处缺陷并给出能抓住它们的测试（[[lcp-rate-limiter-find-the-defect]]、[[lcp-rate-limiter-five-tests]]）。
- 两篇短文写得出机制、代价和多实例的演进（[[lcp-rate-limiter-reflection-lock-atomicity]]、[[lcp-rate-limiter-reflection-multi-instance]]）。

**题解**：[[solution-lcp-rate-limiter]]——先做，再看。经典限流器见 [[solution-rate-limiter]]。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
