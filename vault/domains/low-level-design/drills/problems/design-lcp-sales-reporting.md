---
nodes: [lcproject.lcp-sales-reporting, structure.storage, errors.boundary-validation]
tags: [problem]
---
# Drill：销售报表（Sales Reporting）

一个销售数据库里，每一行是一次购买，同一个客户可以出现在很多行；运营给一个日期区间和几个可选筛选，要三个总数和三个排行榜。
底层是 SQLite，过滤、去重计数、分组、求和、排序、限量都要在数据库里完成，请求里的值只能绑定、不能拼接，所有查询返回的行数合计不超过 `32 + 3k`。
你补全 `handle(request, context)`，计划用时 60 分钟。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先读 `starter.py` 文档字符串里的十九条规则，逐条改写成断言。再做路由、请求体校验与三个标量：
  `{"start":"2026-03-01","end":"2026-04-01"}` 在你自己的示例库上得到正确的 `active_customers`、`total_quantity`、`total_spend_cents`；
  `2026-02-30`、`20260101`、`end` 不晚于 `start` 都是 400 `invalid_request`；`GET /report` 是 404 `not_found`；没有匹配行时三个标量是 0。
- 第 2 关（约 15 分钟）：三个排行。数值降序、平局按键升序、先排序再截到 k；造一个并列的例子，`k=1` 时必须取编号小的那个；
  商品名用 `Zebra`、`apple`、`é` 检查字节序；`k` 的 `1.0`、`1e0` 合法，`null`、`true`、`1.5`、`21` 是 400。
- 第 3 关（约 15 分钟）：三个筛选。`status`、`region`、`item` 精确匹配，`te%` 不是通配符，`x' OR '1'='1` 一行也匹配不上；请求值（包括 `status` 的 `active`）不能以字面量出现在任何语句里，语句里的常量也走绑定；
  具体的 `region` 匹配不到 NULL 地区，不给 `region` 时它们照常参与；筛选对标量与三个排行同时生效。
- 第 4 关（选做，约 15 分钟）：行数预算与边界。用一个记录每次查询的上下文，核对 `k` 取 1、10、20 时所有查询返回的行数合计 ≤ `32 + 3k`；
  `end=2100-01-01` 能报出 2099-12-31；100 个码点的地区合法、101 个非法；不合格的行（缺日期、缺状态、未知状态、`refund`）永远不算。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-sales-reporting/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-sales-reporting -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把十九条规则和第 1 关的例子交给它，一次只给它一个失败的测试：
先路由与校验，再标量，再排行，最后筛选。"资格与筛选只写一份"、"平局键写进 `ORDER BY`"、"值只绑定不拼接"这三个决定自己留着，写进给它的指令里。
每次改动之后先跑全部测试，再读 diff：它有没有把总额写成价格乘数量、有没有用 `COUNT(*)` 数客户、有没有漏掉平局键、有没有把值拼进 SQL、有没有用 `isinstance(k, int)` 放过布尔、有没有改测试。
最后自己写那几个最要紧的测试（并列取小编号、NULL 地区、混合状态的客户只数一次），不要让它代写。

**评分点**
- 开工前把合同定成规则：谁算数、区间左闭右开与哨兵、`k` 与筛选的校验、平局与空结果、错误形状（[[lcp-sales-reporting-contract-rules]]）。
- 说得出状态与不变量：不存状态、一份 `MATCHING` 被四条查询共用、请求冻结成一份参数、行数由语句形状保证（[[lcp-sales-reporting-state-and-invariant]]）。
- 说清怎样一致地筛选、绑定与限行：`$name` 绑定、表名可拼值不可拼、聚合留在数据库里、`1 + 3k` 小于 `32 + 3k`（[[lcp-sales-reporting-reflection-query-design]]）。
- 说清怎样为"客户被重复计数"这类错误设计测试：手算期望、拒绝哪几种错误实现、状态筛选一并钉住（[[lcp-sales-reporting-reflection-verification]]）。

**题解**：[[solution-lcp-sales-reporting]]——先做，再看。同类的有 [[solution-lcp-url-shortener]]（SQLite 与严格校验）和 [[solution-lcp-issue-creation-api]]（HTTP 合同与错误优先级）。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
