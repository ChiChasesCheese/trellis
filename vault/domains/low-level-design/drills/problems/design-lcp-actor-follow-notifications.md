---
nodes: [lcproject.lcp-actor-follow-notifications, patterns.observer, concurrency-depth.compound-actions, data.defensive-copy, errors.boundary-validation]
tags: [problem]
---
# Drill：关注演员与新片通知修复（Actor Follows & Notifications）

CastWatch 让用户关注演员，新片登记时给关注者发站内通知。服务只有四个方法（`follow`、`unfollow`、`add_movie`、`inbox`），
全部在内存里，规模是几万个用户、几千部电影，多个线程同时调用。这是一个**修复项目**：代码能跑，但通知丢失、取关无效、
重试导入行为混乱、收件箱顺序不对。真正的分数在合同里那些容易漏掉的细节上：空白字符表、冲突与重复的区别、受众去重、并发下的串行等价。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先读 `starter.py` 顶部的十一条规则，**不要先改代码**：对每条规则写一个会失败的测试，让测试把缺陷一个个指出来
  （取关、受众、重复导入与冲突、收件箱顺序、空白判定）。然后逐个修，每修一个重跑全部测试。
- 第 2 关（约 15 分钟）：校验与快照。非法输入在改状态之前抛 `ValueError("invalid_input")`，空白按合同字符表而不是 `strip()`；
  卡司入参在调用时就复制；返回的收件箱是副本；`Notice` 不可变；取关后空集合不留在索引里。
- 第 3 关（约 15 分钟）：并发。同一部电影被 32 个线程同时导入，恰好一个 `True`、每个关注者恰好一条通知；
  取关与登记同时发生，结果必须等价于某个串行顺序。用 `threading.Barrier` 起跑，不用 `sleep`。
- 第 4 关（选做，约 15 分钟）：写出 REFLECTION 的三篇短文（原子边界、事务发件箱、千万关注者），再回答追加需求：
  收件箱要能标记已读并按游标分页，它落在哪个类里，哪些代码不用动。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-actor-follow-notifications/starter.py` 里的缺陷修掉，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-actor-follow-notifications -q`。

**和编程智能体一起练**：用 Claude Code 或工作区自带的智能体打开 `starter.py`。第一条指令给它合同的规则和一个具体的失败例子，
一次只让它修一个缺陷、只给一个失败测试；锁的范围、校验和冲突谁先、受众怎么算这些决定你自己留着。每次改动之后先跑测试，
再读 diff：它有没有改测试、有没有把写入挪到锁外、有没有把内部列表直接返回。并发相关的结论不要信它的一句"线程安全"，用你自己的屏障测试验收。

**评分点**
- 先让测试指出缺陷，再逐个修，每次只改一件事并重跑全部测试（[[lcp-actor-follow-notifications-contract-rules]]）。
- 受众是卡司关注者的并集，每人一条；子集判断和逐演员追加都是错的（[[lcp-actor-follow-notifications-contract-rules]]）。
- 重复导入返回 `False` 且不留痕，冲突抛 `movie_conflict` 且状态不变，校验先于冲突（[[lcp-actor-follow-notifications-contract-rules]]）。
- 空白判定用合同的字符表，不用 `strip()`；校验在改状态之前，入参先复制再校验（[[lcp-actor-follow-notifications-contract-rules]]）。
- 一个临界区罩住判重、算受众、写电影、写收件箱；结果等价于某个串行顺序（[[lcp-actor-follow-notifications-contract-rules]]、[[lcp-actor-follow-notifications-reflection-atomic-boundary]]）。
- 状态三块各用合适的结构，核心不变量说得清，空集合立刻删除（[[lcp-actor-follow-notifications-state-and-invariant]]）。
- 只有五个测试的时间，选得出钉住最多规则的五个，并发用屏障（[[lcp-actor-follow-notifications-contract-rules]]）。
- 扩展落点说得清：已读与分页只动收件箱；发件箱和超大演员各有推拉取舍（[[lcp-actor-follow-notifications-contract-rules]]、[[lcp-actor-follow-notifications-reflection-outbox]]、[[lcp-actor-follow-notifications-reflection-ten-million-followers]]）。

**题解**：[[solution-lcp-actor-follow-notifications]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
