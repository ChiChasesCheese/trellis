---
nodes: [lcproject.lcp-review-moderation, errors.exceptions-vs-values, concurrency-depth.compound-actions, data.invariants, testing.partitioning]
tags: [problem]
---
# Drill：评论审核修复（Comment Moderation）

一个评论服务在新建和编辑时都要先问外部审核器，累计被拒三次的用户永久封禁。现有代码能跑，但审核器拿到的是改成小写的内容、被拒时违规数被写成 1、封禁门槛是"大于三"、审核器出错时评论照样发布、编辑成功不加版本。规模是一个类、几十行；难点是五处缺陷叠在同一条路径上：最常见的三次被拒场景里，违规数永远停在 1，封禁永远不会触发，所以只看最后一个返回值分不清是哪一处错了。

**分关要求**（每关做完再看下一关，像真实的修复轮）
- 第 1 关（约 15 分钟）：先不改代码，把八条规则逐条对照现有代码，写出差异清单，并把每处缺陷用一个最小例子在起始代码上跑出来。起始代码已经做对的（输入校验、`404` 先于 `403`、快照拷贝、被拒不占 id、整段加锁）各写一个测试守住。再修两处最直接的：审核器收原文、违规数在原值上加一。
- 第 2 关（约 15 分钟）：修封禁与顺序：第三次被拒仍报 `content_rejected`，状态变成 `3 / True`；之后合格的写入报 `user_blocked`，不问审核器、不加违规。每个边界写两个测试：第二次与第三次，被封前一格与被封后一格；编辑的五步顺序各用一个"同时犯两个错"的请求钉住。
- 第 3 关（约 15 分钟）：修审核器出错与版本：`Exception` 变 `503`、什么都不改、不算违规，`KeyboardInterrupt` 照常穿过；编辑成功版本加一，内容相同也加。再写并发测试：十六个线程用同一个用户同时提交违规内容，审核器睡几毫秒，断言恰好三次拒绝、三次审核器调用。
- 第 4 关（选做，约 15 分钟）：写三个书面回答：被拒的编辑与那一次违规计数之间的原子边界在哪里；审核器变成远程服务、会超时时合同要怎么变；违规数怎样跨重启保留。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-review-moderation/starter.py` 当作要修的服务，改完后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-review-moderation -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给规则和两个数字例子（三次被拒后 `strikes=3`；第四次干净内容得到 `user_blocked`），要求它先列出代码与规则的差异、不改代码；你核对清单后，一次只让它修一类缺陷、只给它一个失败的测试，改完立刻运行测试。封禁的边界、审核器出错算不算违规、锁要罩住多大一段这些决定自己留着；期望值自己独立写出，不接受"把测试改成通过"。

**评分点**
- 写得出开工前的合同：审核器收原文、违规数永久、第三次起封禁、两条固定的校验顺序、失败不留痕、审核器出错是 503（[[lcp-review-moderation-contract-rules]]）。
- 说得清服务要记什么，以及"判决与那一次违规计数同一个临界区"这条不变量，并能解释为什么锁要罩住审核器调用（[[lcp-review-moderation-state-and-invariant]]）。
- 知道审核器变成远程服务之后，锁外调用、锁内复核、合同变弱的那一条、幂等键（[[lcp-review-moderation-reflection-checker-timeout]]）。
- 知道违规数放进数据库时用原子自增并以返回值判断封禁，评论与违规同一个事务（[[lcp-review-moderation-reflection-durable-strikes]]）。
- 写得出能抓住缺陷的测试：大小写敏感的审核器、第二次与第三次的边界、审核器宕机后检查评论与违规数、让审核器变慢的并发测试（[[lcp-review-moderation-contract-rules]]、[[lcp-review-moderation-state-and-invariant]]）。

**题解**：[[solution-lcp-review-moderation]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
