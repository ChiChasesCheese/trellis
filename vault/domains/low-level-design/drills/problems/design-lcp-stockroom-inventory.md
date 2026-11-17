---
nodes: [lcproject.lcp-stockroom-inventory, structure.storage, api.error-contract, errors.boundary-validation, concurrency-depth.compound-actions]
tags: [problem]
---
# Drill：库存 API 修复（Inventory API）

一个私有的库存接口，每个用户管理自己的条目：创建、读取、列出、修改、删除。线上现象是创建成功后条目消失、更新返回旧数据、用户能读到别人的条目。
规模是一个服务类加一个存储集合；难点是几处缺陷叠在一起，而且"版本比较"和"唯一性"只在并发下才露馅。

**分关要求**（每关做完再看下一关，像真实的修复轮）
- 第 1 关（约 15 分钟）：先不改代码，把九条规则逐条对照现有服务，写出差异清单（创建、数量、所有者、更新返回值、重复键的错误映射：一共五处），再跑一遍测试看哪些失败。每处缺陷先写一个会失败的测试。
- 第 2 关（约 20 分钟）：修创建与读取：先写库、再返回库里读出的值；非法数量不能悄悄变 0；每个读、改、删的查询都带 owner，别人的条目与不存在同样是 404。
- 第 3 关（约 20 分钟）：修更新与错误映射：先校验整个请求，再按 owner 找条目，最后比版本；起始代码的检查与加一已经在同一次库操作里，保持；返回更新后的文档；没命中时区分 404 与 409；重复 SKU 是 409（模式校验失败的 400 起始代码已经对了），其余存储错误是 503，响应体里没有异常文本。
- 第 4 关（选做，约 15 分钟）：并发：十六个线程同版本更新恰好一个成功；同一个 SKU 并发创建恰好一个成功；再用两个独立的服务实例连同一个数据库做一遍。然后写三个书面回答：唯一性为什么要数据库保证；构造字典、插入、更新三者的区别；重试安全的增量调整和设置绝对值的区别。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-stockroom-inventory/starter.py` 里的 `InventoryService` 当作要修的服务（集合与辅助函数是固定的），改完后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-stockroom-inventory -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给九条规则和几个数字例子（创建后立即读取、别人读不到、同一版本更新两次得到 200 与 409），要求它只列出代码与规则的差异、不改代码；你核对清单后，一次只让它修一类缺陷、只给它一个失败的测试，改完立刻运行测试。
检查与修改怎样放进同一次库操作、404 与 409 谁先、错误按码映射这些设计决定自己留着；期望值自己独立写出，不接受"把测试改成通过"，也不让它把测试指到真实的库上去清库。

**评分点**
- 写得出开工前的合同：检查顺序、每个查询带 owner、先校验后碰库、版本在库里比、唯一交给索引、错误按码映射（[[lcp-stockroom-inventory-contract-rules]]）。
- 说得清服务不存状态、库里存什么，以及"拼字典、插入、更新"三件事的区别和"同一版本上的并发写只有一个成功"这条不变量（[[lcp-stockroom-inventory-state-and-invariant]]）。
- 知道多进程下唯一性与版本由数据库裁决：唯一索引加条件更新，而不是先查后写或进程内的锁（[[lcp-stockroom-inventory-reflection-concurrent-uniqueness]]）。
- 知道增量调整为什么不幂等，以及用操作号加唯一约束让重试安全（[[lcp-stockroom-inventory-reflection-retry-safe-adjustments]]）。
- 写得出能抓住缺陷的测试：创建后立即读取、别人读不到且条目纹丝不动、返回的是更新后的值、屏障下的同版本并发（[[lcp-stockroom-inventory-contract-rules]]、[[lcp-stockroom-inventory-state-and-invariant]]）。

**题解**：[[solution-lcp-stockroom-inventory]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
