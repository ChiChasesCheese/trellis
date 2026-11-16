---
nodes: [lcproject.lcp-stack-trace-stream, python.context-iterators, fsm.persistence, errors.boundary-validation]
tags: [problem]
---
# Drill：流式调用栈处理器（Streaming Stack Trace Processor）

一个采样式性能分析器每隔一小段时间记录一次调用栈。你要把相邻采样的差别转成有序的 start/end 事件，可以要求"连续 N 次才确认"，
惰性地处理任意长的输入且内存只与栈深有关，把相邻相同的栈合并成段，并支持把状态导出成快照、从快照续跑。计划用时 60 分钟，最后留出时间写三篇关于采样局限与乱序的短文。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先读合同，把 `starter.py` 文档字符串里的七条规则逐条改写成自己的断言。`confirmations=1` 的转换：
  `("main","read")` 之后是 `("main","write")` 得到 `end read`、`start write`（旧后缀从叶到根结束，新后缀从根到叶开始，时间戳是当前采样的）；
  帧由完整前缀识别，所以 `("a","x")` 变成 `("b","x")` 时 `x` 也要先结束再开始；空栈结束全部；输入耗尽不补结束。
- 第 2 关（约 15 分钟）：确认。`confirmations=2` 时 `("main",)` 出现第二次才有 `start main`，时间戳是第二次的；
  父帧保留自己的次数，中断就清零，分开的两段不累加；未确认的帧永远没有结束事件；`confirmations` 为 0、负数、`True`、`1.0` 都是 `ValueError`。
- 第 3 关（约 15 分钟）：惰性与压缩。`convert_samples` 在开始迭代之前不读任何采样，当前采样的事件没产完不读下一个，不留历史；
  `compress_samples` 把相邻相同的栈合成 `StackRun(start, end, stack, count)`，读到第一个不同的采样就先产出前一段，空栈合法，不相邻的相同栈是两段。
- 第 4 关（约 15 分钟）：校验与快照。时间戳是精确的 int 或 float、有限、非负、严格递增，大整数按精确数值比较，名字必须是非空字符串；
  失败的 `feed` 不消耗时间戳。`snapshot()` 恰好五个键，`from_snapshot` 先校验再恢复，从快照续跑的输出与不中断完全一样。
  选做：用随机流和每一个快照点写出"续跑相同"的属性测试，再写短文回答采样的局限、只看最后 N 个采样的代价和乱序采样的处理。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-stack-trace-stream/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --no-project --python 3.11 --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-stack-trace-stream -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把七条规则和第 1、2 关的小例子交给它，一次只给它一个失败的测试，
先让它做 `confirmations=1`，再加确认。"帧由完整前缀识别""已确认就是连续次数等于 N、不另存标志""先校验再改状态""快照就是全部状态"这几个设计决定自己留着，写在给它的指令里。
每次改动之后先跑全部测试，再读 diff：它有没有改测试、有没有改公开签名、失败的 `feed` 有没有先动了状态、`snapshot` 返回的列表是不是内部列表本身。
最后自己写那几个最要紧的测试（递归同名帧、根变了的同名叶子、确认中断清零、2**53 与 2**53+1 的时间戳、每个快照点的续跑），不要让它代写；
可以让它另写一个只看完整历史、不带状态的参照模型，再用随机流把两者对在一起。

**评分点**
- 开工前把合同定成规则：帧按完整前缀识别、先结束后开始、连续 N 次才确认、先校验再提交、快照续跑逐字相同（[[lcp-stack-trace-stream-contract-rules]]）。
- 说得出要存的状态：上一个栈、每层前缀的连续次数（封顶 N）、上一个时间戳；已确认由次数推出、不另存标志；校验全部通过之后才写（[[lcp-stack-trace-stream-state-and-invariant]]）。
- 快照与恢复各复制一份列表，恢复后下一个时间戳必须严格更大，非法快照一律 `ValueError`（[[lcp-stack-trace-stream-state-and-invariant]]）。
- 说清采样还原不了什么：比采样间隔短的调用、两个采样之间的顺序与起止；只看最后 N 个采样为什么会丢掉确认状态（[[lcp-stack-trace-stream-reflection-what-samples-know]]）。
- 说清乱序采样怎么处理而内存仍然有界：转换器前面的最小堆加水位线，迟到太久的丢弃并计数（[[lcp-stack-trace-stream-reflection-out-of-order]]）。
- 给编程智能体的第一条指令带着合同和小例子，拆小步，自己留着确认与快照的语义，并用随机流证明续跑相同（[[lcp-stack-trace-stream-contract-rules]]）。

**题解**：[[solution-lcp-stack-trace-stream]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
