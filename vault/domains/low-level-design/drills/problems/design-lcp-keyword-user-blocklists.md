---
nodes: [lcproject.lcp-keyword-user-blocklists, concurrency-depth.compound-actions, data.defensive-copy]
tags: [problem]
---
# Drill：关键词与用户拦截（Keyword & User Blocking）

一个讨论区在每次发帖之前调用内容准入组件：内容含配置的关键词就拒绝，用户在手动封禁名单里或累计被拒三次就封禁。
组件被多个线程同时调用，配置可以在运行中整体替换。计划用时 60 分钟，最后留出时间写三篇关于配置更新顺序、申诉审计和百万级关键词的短文。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先读合同，把 `starter.py` 文档字符串里的十二条规则逐条改写成自己的断言。
  只做配置与匹配：`[" SPAM "]` 下 `check("alice", "SPAM offer")` 得到 `keyword`、`["spam"]`、`strikes=1`；
  裸字符串、`bytes`、非字符串条目、空白条目都抛 400；`ß` 与 `STRASSE`、词尾 `σ` 的例子自己运行一遍再写期望值。
- 第 2 关（约 15 分钟）：`state`、手动封禁、累计违规。第三次被拒仍是 `keyword`，第四次起是 `user_blocked` 且次数停在 3；
  一个请求命中三个词只加一次；干净请求不清零；非法输入的 400 要在判封之前，被封的用户也一样。
- 第 3 关（约 10 分钟）：两个 `replace_*` 整体替换；校验失败时旧配置不变；一次性迭代器可用；迭代中抛出的异常原样传出；
  替换不清零次数，移出手动名单只在次数小于 3 时解封；返回值与两个实例互相隔离。
- 第 4 关（约 20 分钟）：四十个线程用屏障抢同一个用户，每轮恰好三个 `keyword`；配置在两张表之间来回切换时，
  每个请求的 `matches` 是整张旧表或整张新表的结果。选做：把关键词表换成自动机，用随机输入证明结果与逐词扫描一致。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-keyword-user-blocklists/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-keyword-user-blocklists -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把十二条规则和合同里的数字例子交给它，
一次只给它一个失败的测试，先写关键词表与校验，再写账本与 `check`。锁的范围、"被封时不匹配也不加次数"、配置整份替换这三个设计决定自己留着，
写进给它的指令。每次改动之后先跑全部测试，再读 diff：看它有没有用 `lower()` 代替 `casefold()`、有没有给用户 ID 做 `strip()`、
有没有改成正则或词边界、有没有额外存一个 `blocked` 标志、有没有改测试。最后自己写并发测试，不要让它代写。

**评分点**
- 开工前把合同定成规则：先校验输入、再判封、再匹配、一个被拒请求只加一次、干净请求不清零（[[lcp-keyword-user-blocklists-contract-rules]]）。
- 口径说得清：关键词 `strip().casefold()`、内容只 `casefold()`、字面子串、结果排序无重复、用户 ID 原样（[[lcp-keyword-user-blocklists-contract-rules]]）。
- 说得出要保存的状态与最要紧的不变量：次数不超过 3，被封由名单和次数算出来（[[lcp-keyword-user-blocklists-state-and-invariant]]）。
- 用一把锁罩住判封、匹配、记账，配置在锁外读、锁内换一个引用，请求看到整份旧表或新表（[[lcp-keyword-user-blocklists-state-and-invariant]]）。
- 给编程智能体的第一条指令带着合同和数字例子，一次一个失败用例，锁的范围等决定自己留着（[[lcp-keyword-user-blocklists-contract-rules]]）。
- 申诉不丢审计：违规只追加成事件，撤销也是事件，次数改成查询，账本接口不变（[[lcp-keyword-user-blocklists-reflection-appeals-audit]]）。
- 关键词变成百万级：逐词扫描线性变慢，换自动机，后台建好再换引用，内存成为新瓶颈（[[lcp-keyword-user-blocklists-reflection-million-keywords]]）。

**题解**：[[solution-lcp-keyword-user-blocklists]]——先做，再看。每个 key 一份状态的相邻题见 [[solution-lcp-rate-limiter]]。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
