---
nodes: [lcproject.lcp-image-transform-pipeline, concurrency.patterns, python.context-iterators, concurrency-depth.testing, errors.cleanup]
tags: [problem]
---
# Drill：图片变换流水线（Image Transform Pipeline）

一个批量图片服务把每张原图依次过同一条变换链，不同的图并发处理；输出必须保序，一张图坏了不能拖累别的图，同时在途的原图字节有预算，输入是只能读一遍的迭代器。规模是一个类加一个小的准入类、两百行；难点是准入的三个边界（先进先出、预算、超大队头）和"最多"类规则怎么测，线程池只是执行层。

**分关要求**（每关做完再看下一关，像真实的构建轮）
- 第 1 关（约 15 分钟）：单张图与有序结果，不并发。变换按顺序各调用一次、输出接输入、空链是恒等；`Exception` 变成 `data=None` 加 `"类型名: 消息"`（空消息、多行消息原样保留），后面的变换不再调用；`BaseException` 原样冒出；`index` 从 0 起，重复 `image_id` 照样各占一项。先写 README 的例子当测试，再写失败路径。
- 第 2 关（约 10 分钟）：线程池与保序。按下标放进结果表，最后按 `0..n-1` 取出；用事件把完成顺序强制成输入顺序的反面，再用屏障让 `max_workers` 张图同时在场（串行实现在这里挂住）。
- 第 3 关（约 15 分钟）：先进先出准入与字节预算。写 `AdmissionWindow`：名额、预算、恰好等于预算要放行、在途为空时超大队头独自进入并排斥一切、拒绝不改状态；先写它的纯逻辑单元测试，再接进循环。失败路径也要还字节。
- 第 4 关（选做，约 10 分钟）：惰性取用与有界提交。只在有名额时才向迭代器要下一项，队头放不进去就原地不动；全部阻塞时要过的输入不超过 `max_workers + 1`。再写三个书面回答：先进先出与吞吐的取舍、一百万张图的分布式切分与幂等键、生产里除输入字节外要测的内存。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-image-transform-pipeline/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-image-transform-pipeline -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给十三条规则和三个数字例子（README 的三张图；预算 10 时 5 加 5 能同时在途；预算 1 时两张 50 字节的图各自独自运行），要求它先说每条规则会落在哪个方法里，不写代码。你核对后，一次只让它做一关、只给它一个失败的测试，改完立刻运行测试。准入规则（先进先出、超大队头的出口）、"失败也还字节"、协调线程独占状态这几个决定自己留着；期望值自己独立写出；别让它用 `Executor.map` 或 `list(jobs)`，也别让它用 `sleep` 写并发测试；最后让它故意把 `>` 改成 `>=`、再把"窗口空了就放"删掉，各一次，确认测试会变红。

**评分点**
- 开工前写得出合同：结果按下标、失败只停一张图、`BaseException` 原样冒出、worker 上限是上限也是下限、先进先出、预算计原图字节、惰性取用（[[lcp-image-transform-pipeline-contract-rules]]）。
- 说得清一次 `run` 要记什么、谁来改：窗口、在途表、结果表、队头，协调线程独占，工作线程只返回值；以及"在途数与在途字节"这条不变量和失败路径也要还账（[[lcp-image-transform-pipeline-state-and-invariant]]）。
- 讲得出先进先出的代价与折中：超大队头独占窗口时其余 worker 空转，越过队头会饿死队头，有界越过、预算留余量、大图单独队列（[[lcp-image-transform-pipeline-reflection-scheduler-fairness]]）。
- 讲得出一百万张图怎么分布式：按下标分片、幂等键是（批次号，下标）而不是 `image_id`、确定的输出键、清单最后写、片内保序（[[lcp-image-transform-pipeline-reflection-distributed-batch]]）。
- 写得出能抓住缺陷的测试：屏障证明"至少"、纯逻辑窗口测试证明"最多"、迭代器里检查取用数、与顺序实现对拍；并知道线程层面的"最多"只对正确实现确定（[[lcp-image-transform-pipeline-contract-rules]]、[[lcp-image-transform-pipeline-state-and-invariant]]）。

**题解**：[[solution-lcp-image-transform-pipeline]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
