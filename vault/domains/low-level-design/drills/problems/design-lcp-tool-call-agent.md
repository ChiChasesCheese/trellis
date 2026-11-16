---
nodes: [lcproject.lcp-tool-call-agent, concurrency.patterns, errors.exceptions-vs-values]
tags: [problem]
---
# Drill：可靠的工具调用智能体（Reliable Tool-Calling Agent）

一个智能体循环：把对话交给模型，模型要么回答，要么请求一批工具；循环并发执行这批工具、把结果按顺序写回对话，再交给模型，直到模型不再请求工具。
模型和工具都是传进来的普通可调用对象；要保证记录有序、重复调用只执行一次、畸形输出被拒绝、轮数与调用数有预算。计划用时 60 分钟，最后留出时间回答三个反思问题。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先读合同，把 `starter.py` 文档字符串里的十三条规则逐条改写成自己的断言。然后只做单线程循环：
  两个价格查询加一次最终回答，记录依次是 user、assistant、tool、tool、assistant，`model_calls` 为 2，`tool_calls` 为 2；空文本的回答也是终止。
- 第 2 关（约 15 分钟）：错误与校验。未知工具得到 `{"ok": False, "error": "unknown_tool"}`，工具抛错或返回元组得到 `tool_error` 且不含异常文本；
  响应里前一个调用合法、后一个含 NaN，则前一个工具也不能执行。
- 第 3 关（约 15 分钟）：重放与预算。同 ID 同名同参（键顺序不同也算）只执行一次；`1` 对 `1.0` 是冲突；
  `max_tool_calls=2` 时，第二个响应带两个新 ID，抛 `tool budget exceeded` 且这两个工具都没执行；`max_turns=1` 且模型仍要工具，处理完这批再抛 `model budget exceeded`。
- 第 4 关（约 15 分钟）：并发与所有权。用线程池，上限 `max_workers`；用屏障证明三个调用能重叠，用事件链让完成顺序反过来而结果顺序不变；
  模型改自己的快照、工具改自己的参数，都不能改动记录和缓存。选做：工具抛 `BaseException`。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-tool-call-agent/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-tool-call-agent -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把十三条规则和 README 的例子交给它，
一次只给它一个失败的测试，先让它写单线程循环，再逐条加错误、重放、预算、并发。预算的报错时刻、「状态只由一个线程写」、
`BaseException` 的规则这些设计决定自己留着，写在给它的指令里。每次改动之后先跑全部测试，再读 diff：它有没有改测试、有没有改公开签名、
有没有把并发写成顺序循环、有没有把异常文本放进结果。最后自己写屏障测试和反序完成的测试，不要让它代写。

**评分点**
- 开工前把合同定成规则：先预检再执行、结果按请求顺序、同 ID 只执行一次、错误是结果、两个预算的报错时刻、深拷贝（[[lcp-tool-call-agent-contract-rules]]）。
- 说得出状态与不变量：一个 ID 一条缓存、尝试数等于缓存条目数、只有主线程写记录和缓存（[[lcp-tool-call-agent-state-and-invariant]]）。
- 重放的判据用规范化 JSON 文本，不用 `dict` 相等，因为 `1` 与 `1.0` 会被当成同一个（[[lcp-tool-call-agent-contract-rules]]）。
- 预检在启动线程之前：冲突与预算超额时零执行，之前的批次不回滚（[[lcp-tool-call-agent-state-and-invariant]]）。
- 给编程智能体的第一条指令带着合同和例子，拆小步，自己留着预算与线程的决定（[[lcp-tool-call-agent-contract-rules]]）。
- 内存缓存在重启后失效：先写意图、调用 ID 做幂等键、`pending` 表示结果未知（[[lcp-tool-call-agent-reflection-irreversible-restart]]）。
- 模型与工具不可信时，沙箱进程、墙钟超时、授权和输出上限放在循环之外（[[lcp-tool-call-agent-reflection-untrusted-safeguards]]）。

**题解**：[[solution-lcp-tool-call-agent]]——先做，再看。线程池的经典题目见 [[solution-thread-pool]]。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
