---
nodes: [lcproject.lcp-payment-reconcile-api, errors.retry, concurrency-depth.compound-actions]
tags: [problem]
---
# Drill：付款对账服务（Payment Reconciliation）

一个对账平台把银行付款匹配到未付发票：客户可能重发同一笔付款，几笔付款可能同时抢同一张发票，运营还会一次提交一整批付款，要么全入账、要么一笔都不动。
你补全进程内的 `ReconciliationService`，HTTP 适配器已经写好。计划用时 60 分钟，最后留出时间写三篇关于多实例原子性、键过期和匹配索引的短文。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先把 `starter.py` 文档字符串里的九条规则逐条用自己的话改写成断言，再做登记。
  `register_invoices(["ORD A, 2026-08-04, 100", "ORD B, 2026-08-05, 100"])` 返回 `(201, {"registered_count": 2})`；
  格式错得到 `400 invalid_input`，重复的号得到 `409 duplicate_invoice`，而且一批里出任何错都一张不存；`list_invoices` 按到期日、再按发票号排序。
- 第 2 关（约 20 分钟）：三级匹配。`"rcpt_3, 147, wire transfer"` 容差 3 命中 `LN-1`（150）并标 `fuzzy`，容差 2 则 `UNMATCHED`；
  金额相等总是先于容差；备注里的 `paying for: ORD A` 不看金额，且标记不分大小写（`PAYİNG FOR:` 也算）。
  同级平局先比到期日、再比金额差、最后比发票号：四张发票 `A 03-02 101`、`B 03-01 96`、`D 03-01 102`、`C 03-01 98`，付 100 容差 5，依次得到 `C D B A`。
- 第 3 关（约 15 分钟）：幂等。同键同请求再发一次得到 `(200, 当初那份响应)`，哪怕之后新登记了发票；同键不同金额得到 `409 idempotency_conflict`；
  非法请求带着用过的键得到 `400`；没有键的请求每次都重新匹配。
- 第 4 关（约 10 分钟）：`reconcile_batch`。`[p1 带键 retry-1, p1 带键 retry-1, p2]` 的行状态是 `[201, 200, 201]`；
  `[p3 带键 new-key, "invalid"]` 得到 400，而且 p3 的结算和 `new-key` 都被撤销。然后并发：六十四个线程同一个键只结算一次，批次中间状态不被读到。选做：过期键、匹配索引。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-payment-reconcile-api/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-payment-reconcile-api -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把九条规则和每关的数字例子交给它，
一次只给它一个失败的测试：先登记，再三级匹配，再幂等，最后批次。校验顺序（先校验请求再查键）、锁的范围（整批持锁）、批次怎么回滚（撤销日志还是拷贝账本）这三个设计决定自己留着，写在给它的指令里。
每次改动之后先跑全部测试，再读 diff：它有没有改测试、有没有整串 `lower()` 备注、有没有用浮点数算金额、幂等比较是不是只比了付款号、锁里有没有多出或少了步骤。
最后自己写那几个最要紧的测试（同键重放不再结算、批次失败后键也没留下、屏障并发同键只结算一次），不要让它代写。

**评分点**
- 开工前把合同定成规则：先校验再查键、三级优先级与平局顺序、标记不分大小写且位置取自原串、幂等指纹与 409、批次逐行与第一个错误胜出（[[lcp-payment-reconcile-api-contract-rules]]）。
- 说得出状态与不变量：有序发票加字典、回执表、撤销日志、一把锁；一张发票至多结算一次，批次对外全有或全无（[[lcp-payment-reconcile-api-state-and-invariant]]）。
- 多实例部署时批次怎么保持原子：一个数据库事务、`settled_by IS NULL` 的条件更新、键上的主键约束（[[lcp-payment-reconcile-api-reflection-multi-instance-batch]]）。
- 幂等键怎么过期又不重复结算：保留期大于重试窗口，键带时间戳，过期的键被拒绝而不是当成新键（[[lcp-payment-reconcile-api-reflection-key-expiry]]）。
- 并发测试写成不变量：屏障起跑、一个 201 加六十三个 200、读到的只会是全未付或全已付（[[lcp-payment-reconcile-api-state-and-invariant]]）。

**题解**：[[solution-lcp-payment-reconcile-api]]——先做，再看。同样是"重试与幂等"的服务见 [[solution-lcp-issue-creation-api]]，整批全有或全无的账本见 [[solution-lcp-scheduled-banking]]。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
