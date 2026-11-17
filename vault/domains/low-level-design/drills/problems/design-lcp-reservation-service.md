---
nodes: [lcproject.lcp-reservation-service, concurrency-depth.compound-actions, fsm.illegal-transitions, errors.narrow-catch, debugging.hypothesis, ai.verification]
tags: [problem]
---
# Drill：预约服务线上事故（Reservation Service Incident）

一个课程预约服务已经上线：用户预约、取消、在 Dashboard 查看自己的预约。客服反馈重试之后名额被占两次、放票时名额互相矛盾、取消之后页面自相矛盾，生产库里还有对不上的历史记录，而且生产库不能重置。规模是三个服务函数、四张表、一个迁移；难点是几类缺陷互相叠加，必须先复现、再修、再原地修数据。

**分关要求**（每关做完再看下一关，像真实的事故排查）
- 第 1 关（约 12 分钟）：先不改代码，把日志和客服反馈翻成失败的测试：重试得到两条 active、重复取消后名额超过容量、不存在的场次返回 500、别人能取消、"进行中"列表里有已取消。再逐条修：场次存在 → 是否已持有 → 是否已满；取消先看主人再看状态；列表按状态过滤。
- 第 2 关（约 12 分钟）：让三件事同成败并经得起并发：状态、名额、审计放进一个事务，先锁场次再检查再写，名额用相对更新。写一个真线程加屏障的测试：12 个用户抢容量 3 的场次，断言恰好 3 个成功、名额 0、审计 3 行。
- 第 3 关（约 12 分钟）：写第二个迁移（真实工作区没有这部分，`starter.py` 里的 `plan_repair` 与 `upgrade_0002` 是空桩，要自己写）：先修历史数据（去重留最早、超容量按同序留到上限、同一个 `cancelled_at`、不补审计、重算计数），再建部分唯一索引和 `available_slots <= capacity`。修复要带 dry-run，并且连跑两次第二次什么都不改；每个规则写一个测试。
- 第 4 关（选做，约 9 分钟）：写生产变更记录：改了什么、预演看到什么、回滚方案、验证结果；再回答：快照里没有容量为 0 的场次时，排练通过说明了什么、没说明什么。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-reservation-service/starter.py` 当作要修的服务（它带着和线上同类的缺陷），改完后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-reservation-service -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给规则和一个数字例子（容量 3 的场次，同一用户预约两次，第二次必须 409），要求它先列出代码与规则的差异、不改代码；你核对清单后，一次只让它修一类缺陷、只给它一个失败的测试，改完立刻运行测试。加锁的位置、检查的先后、修复规则的顺序这些设计决定自己留着；期望值自己独立写出，不接受"把测试改成通过"。碰生产库之前，自己逐字读 dry-run 的输出，再让智能体帮你起草变更记录。

**评分点**
- 写得出开工前的合同：预约的判断顺序与 409/404、名额恒等式、取消按主人隔离且幂等、三件事同成败、修复规则（[[lcp-reservation-service-contract-rules]]）。
- 说得清要存什么：名额是冗余计数器，恒等于容量减 active 数，唯一索引与 CHECK 让数据库兜底（[[lcp-reservation-service-state-and-invariant]]）。
- 知道放票时怎么不超卖：先锁场次行、再检查、后写三件事，相对更新，取消同序，只把唯一冲突翻成 409（[[lcp-reservation-service-concurrent-booking]]）。
- 写得出可预演、可重复运行的数据修复：计划与应用分开，先去重再按容量，先数据后约束，一个事务，dry-run 回滚（[[lcp-reservation-service-data-repair]]）。
- 写得出能抓住缺陷的测试：整库快照比较、真线程加屏障、第二次运行不变、中途失败回到原样（[[lcp-reservation-service-concurrent-booking]]、[[lcp-reservation-service-data-repair]]）。

**题解**：[[solution-lcp-reservation-service]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
