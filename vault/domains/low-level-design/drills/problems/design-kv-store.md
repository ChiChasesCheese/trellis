---
nodes: [problems.components.kv-store, structure.storage]
tags: [problem]
---
# Drill：内存键值存储（In-Memory Key-Value Store）

一个进程内的键值存储：每个 key 下面是一张字段表，而不是一个裸值。规模是百万级 key、
十层以上的嵌套事务。和[[solution-bank-account|银行账户系统]]一样是分关递进的机考题——
做完一关再看下一关，别提前偷看后面的需求。**这道题真正加进来的东西不是又一种查询**，
而是"每一次改动都要能被撤销"——这句话从第 1 关就该刻进实现里，不是留到第 4 关再补。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：`set(timestamp, key, field, value)`／`get`／`delete`，以及"有
  多少个 key 的某个字段等于某个值"的统计查询。想清楚删除一个不存在的字段该报错还是静默
  成功，两种选择都要能说出理由。
- 第 2 关（约 15 分钟）：按前缀扫描 key、列出一个 key 的所有字段，都要有**确定的顺序**——
  题面不一定明说，但排序错了在隐藏测试里等于随机挂掉一半用例。
- 第 3 关（约 20 分钟）：给字段加 TTL，再给整个 key 加一条独立的 TTL；一切由传入的
  `timestamp` 驱动，过期的数据在下一次任何访问它的调用里被发现并清除，不许起后台线程。
  想清楚这两条过期时间线为什么不能合并成一条。
- 第 4 关（约 25 分钟）：`begin`/`commit`/`rollback`，可以任意深度嵌套；`rollback` 只
  撤销最内层，`commit` 把最内层折叠进上一层。在"撤销日志"和"写时复制的覆盖栈"之间选一个
  实现，并且能说出另一个方案在"存储大、嵌套深"时的代价。事务里设置的 TTL，提交之后要能
  正常过期、回滚之后要像从未发生过——这是检验实现是否正确的最好测试。

**怎么练**：把 `vault/domains/low-level-design/problems/kv-store/starter.py` 的方法体补全，然后在
仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/kv-store -q`。

**评分点**
- 撤销日志和写时复制覆盖栈两个方案都能讲清楚，并且说得出后者在"存储大、嵌套深"时的
  内存和读延迟代价（[[problems-kv-store-undo-log-vs-copy-on-write]]）。
- "把改动真正写入"和"把改动撤销回去"用同一个函数实现，说得出为什么不需要两套逻辑
  （[[problems-kv-store-apply-field-symmetric]]）。
- `commit` 把这一层的撤销记录折叠进上一层，而不是让改动"跳过中间层直接变成永久"
  （[[problems-kv-store-commit-folds-into-parent]]）。
- key 级过期和字段级过期是两条独立判断的时间线，说得出为什么不能合并
  （[[problems-kv-store-two-independent-ttl-lines]]）。
- 过期状态永远是用当前时间重新推导的结论，不是存下来的布尔字段，说得出这为什么让"撤销
  一次惰性清理"总是安全的（[[problems-kv-store-expiry-recomputed-not-cached]]）。
- 认出撤销日志的每条记录本质上是命令模式（Command），并说得出 Python 里为什么用闭包
  而不用专门的类（[[problems-kv-store-undo-log-is-command-pattern]]）。
- 多线程场景下选择给整个存储加一把锁，而不是只锁单次读写的临界区，并说得出原因
  （[[problems-kv-store-single-lock-for-transactions]]）。
- `begin()` 时不会对整个存储做深拷贝，说得出为什么那样做会在存储和嵌套深度变大时最先
  出问题（[[problems-kv-store-begin-deep-copy-mistake]]）。

**题解**：[[solution-kv-store]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
