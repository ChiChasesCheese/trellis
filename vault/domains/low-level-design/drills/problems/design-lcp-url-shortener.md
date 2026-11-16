---
nodes: [lcproject.lcp-url-shortener, structure.storage, api.error-contract]
tags: [problem]
---
# Drill：短链服务（URL Shortener）

一个短链接产品的后端：用户提交长网址换一个短码，别人访问短链时被带到原网址；所有者可以凭令牌删除，运营看点击统计。
底层是 SQLite，几十个请求线程共用一条连接，状态码与 JSON 的形状是合同。你补全 `URLShortener` 与 `Api`，计划用时 60 分钟。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先读 `starter.py` 文档字符串里的十六条规则，逐条改写成断言。再做建表与创建：
  `create("https://example.com/path")` 得到匹配 `[A-Za-z0-9]{6,10}` 的短码、`hit_count` 为 0、以 `tok_` 开头的令牌；
  `https://bad host/path`、`abc\n` 作短码、`True` 作 ttl 都是 `ValidationError`；自定义短码被占用是 `ConflictError`；五次生成都撞是 `CodeGenerationError`。
- 第 2 关（约 15 分钟）：`get`、`resolve_redirect`、`increment_hits` 与过期。`ttl_seconds=60` 的链接在第 59.999 秒活跃、第 60 秒过期；
  过期的跳转抛 `ExpiredLinkError` 且点击不变；过期的链接 `get` 仍然返回、`is_expired` 为真。过期判断与加一要放在同一条 SQL 里。
- 第 3 关（约 15 分钟）：`delete`、`get_stats` 与 HTTP。缺令牌 400、令牌错 403、短码不存在 404（缺令牌先于查短码）；
  统计按点击降序、同分按短码升序，过期的也计入；每个错误都是 `{"error": ...}`；`PUT /links` 是 405，`GET /a/b/c` 是 404。
- 第 4 关（选做，约 15 分钟）：并发。一百个线程同时跳转，点击恰好一百；三十二个线程抢同一个自定义短码，恰好一个成功；
  两个连接打开同一个数据库文件各跳转二十次，点击恰好四十。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-url-shortener/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-url-shortener -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把十六条规则和第 1 关的例子交给它，一次只给它一个失败的测试：
先建表与创建，再跳转与计数，再删除与统计，最后 HTTP。事务的范围、"过期判断与加一在同一条 UPDATE"、"直接插入再接冲突"这三个决定自己留着，写进给它的指令里。
每次改动之后先跑全部测试，再读 diff：它有没有改测试、有没有改公开签名、有没有把过期判断拆成两条语句、有没有用 `match` 加 `$` 校验短码、有没有放过布尔。
最后自己写那几个最要紧的测试（过期的跳转不加点击、缺令牌先于查短码、屏障并发计数恰好），不要让它代写。

**评分点**
- 开工前把合同定成规则：校验、冲突与生成、过期闭区间、删除的判定顺序、统计排序、错误形状（[[lcp-url-shortener-contract-rules]]）。
- 说得出状态与不变量：一张表、主键唯一、点击只在活跃时增加、过期由时间推出、令牌只在创建时返回（[[lcp-url-shortener-state-and-invariant]]）。
- 说清并发计数哪几步必须原子：条件 UPDATE、进程内锁与跨进程事务各管哪一层（[[lcp-url-shortener-reflection-concurrent-hits]]）。
- 说清短码分配：直接插入接冲突、自定义与自动的不同处理、五次上限、随机而非哈希（[[lcp-url-shortener-reflection-code-allocation]]）。

**题解**：[[solution-lcp-url-shortener]]——先做，再看。同类的有 [[solution-lcp-issue-creation-api]]（授权与幂等）和 [[solution-ttl-cache]]（过期）。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
