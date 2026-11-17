---
nodes: [lcproject.lcp-issue-creation-api, errors.retry, concurrency-depth.compound-actions]
tags: [problem]
---
# Drill：可重试的工单服务（Retry-Safe Issue Service）

一个项目管理产品的工单接口：成员在自己的项目里创建工单、在打开与关闭之间切换、按 id 翻页列出。
客户端超时后会带着同一个幂等键重试创建，两个同事可能同时改同一张工单，一个项目的成员看不到别的项目的任何东西。
你补全进程内的 `IssueService`，HTTP 适配器已经写好。计划用时 60 分钟，最后留出时间写三篇关于原子性、键过期和乐观锁的短文。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先读合同，把 `starter.py` 文档字符串里的十二条规则逐条用自己的话改写成断言。
  然后做授权、创建、`get`：`create("mina", "orbit", {"title": " Rotate logs "})` 返回 `(201, {"id": 1, ..., "title": "Rotate logs", "status": "open", "version": 1})`；
  空串用户得到 401、非成员得到 404、乱写的请求体得到 400，而且同时违反时 401 先于 404 先于 400；`get` 取别的项目的工单是 `404 issue_not_found`。
- 第 2 关（约 15 分钟）：幂等。同一个 `(用户, 项目, 键)` 再发规范化后相同的请求，返回 `(200, 当前工单)`，不同则 `409 idempotency_conflict`；
  失败的请求不占键、不耗 id。写一个测试：关闭工单之后重放，应当看到 `status: "closed"`、`version: 2`。
- 第 3 关（约 15 分钟）：`transition`。顺序是授权、查工单、校验状态与版本的格式、比较版本；状态变了版本加一，没变不动，两种情况版本都必须匹配；
  `version=True` 必须是 400。
- 第 4 关（约 15 分钟）：`list` 的游标分页（id 严格大于 `after_id`，先过滤再截断到 `limit`），然后并发：
  六十四个线程用同一个键创建同一张工单，恰好一个 201，列表里只有一条；四十八个线程在版本 1 上同时发 `closed`，恰好一个成功。选做：幂等键过期。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-issue-creation-api/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-issue-creation-api -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把十二条规则和第 1 关的数字例子交给它，
一次只给它一个失败的测试，先做授权与创建，再做幂等，再做版本。校验的顺序、锁的范围、"先校验后写状态"这三个设计决定自己留着，写在给它的指令里。
每次改动之后先跑全部测试，再读 diff：它有没有改测试、有没有改公开签名、锁里有没有多出或少了步骤，有没有把 `bool` 当成整数放过。
最后自己写那几个最要紧的测试（重放返回关闭后的状态、同状态错版本得到 409、屏障并发创建只建一条），不要让它代写。

**评分点**
- 开工前把合同定成规则：授权先于校验、幂等的范围与规范化比较、版本必须匹配、失败不耗 id、bool 不是整数、先过滤再截断（[[lcp-issue-creation-api-contract-rules]]）。
- 说得出状态与不变量：每项目一份升序工单与回执表，一个键至多对应一张工单，读和写都在同一把锁里，对外只给快照（[[lcp-issue-creation-api-state-and-invariant]]）。
- 说清哪几步必须原子：查键、分配 id、追加、记回执；GIL 为什么不够；失败不留痕靠语句顺序（[[lcp-issue-creation-api-reflection-atomic-retry]]）。
- 幂等键过期：保留期大于重试窗口，过期后同键当新键，处理中的请求不能清（[[lcp-issue-creation-api-reflection-key-expiry]]）。
- 版本号冲突检测和数据库里先锁住这一行，各适合什么情况：机制、代价、为什么常并用（[[lcp-issue-creation-api-reflection-optimistic-vs-row-lock]]）。

**题解**：[[solution-lcp-issue-creation-api]]——先做，再看。内存键值存储与任务看板见 [[solution-kv-store]]、[[solution-task-management]]。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
