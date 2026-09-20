---
nodes: [problems.machines.coffee-machine, concurrency.primitives, patterns.observer]
tags: [problem]
---
# Drill：咖啡机（Coffee Machine）

一台放在办公室的多出口咖啡机：几款饮品各有配方，几个出水口**同时**从**同一份**原料库存制作，
原料快用完时要通知运维。这是整套题里最干净的一道并发题——没有调度算法，没有复杂状态机，
所有分数都在**锁的边界**上：临界区到底是哪几行，你有没有把几十秒的冲煮圈进去。
金额用整数分，用量用整数毫升／克。照真实机考的节奏分关来做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 15 分钟）：配方是一张"原料 → 用量"的表，做一杯就是按表扣料。硬要求是
  **全有或全无**：牛奶不够时浓缩一滴都不许被扣掉，冲煮中途故障要把原料原样退回。报错要
  一次说清**每种**原料还差多少。先别碰线程。
- 第 2 关（约 20 分钟）：几个出口同时从同一份库存制作。先想清楚"一杯咖啡要做几十秒"这个
  数量级意味着什么，再决定锁盖住哪几行。验收是两条可断言的不变式：任何原料的余量不为负；
  成功的杯数**恰好**等于库存能支撑的杯数，一杯不多一杯不少。测试用真实线程加
  `threading.Barrier`，不许用 `sleep`。
- 第 3 关（约 15 分钟）：原料跌破警戒线时通知订阅者，事件要**自带发生了什么**（哪种原料、
  还剩多少、警戒线多少），而不是让订阅者回头去查库存。再加补货，让告警能重新武装；并想清楚
  一个细节：如果订阅者在回调里反过来调用这台机器补货，会发生什么？
- 第 4 关（选做）：加一款用到全新原料的饮品，冲煮那条路径**一行都不许改**。如果你发现自己
  要去改一个枚举、改类型标注，回头看第 1 关把原料表示成了什么。

**怎么练**：把 `vault/domains/low-level-design/problems/coffee-machine/starter.py` 的方法体
补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/coffee-machine -q`。

**评分点**
- 说得出临界区只有"算缺口 → 扣 → 看谁跌破线"三步，并解释冲煮为什么必须在锁外（[[problems-coffee-machine-critical-section]]）。
- 扣减是先算全部缺口、再统一扣，绝不边查边扣（[[problems-coffee-machine-all-or-nothing]]）。
- 冲煮失败原样退回，且退回时不再持长锁；出口在 `finally` 里归还（[[problems-coffee-machine-release-after-failed-brew]]）。
- 事件在锁内算、在锁外投递，说得出为什么不能用 `RLock` 去"修"订阅者回调的死锁（[[problems-coffee-machine-publish-outside-lock]]、[[concurrency-lock-while-calling-out]]）。
- 告警事件自带余量和警戒线，订阅者不需要反向查询主体（[[problems-coffee-machine-event-carries-what-happened]]）。
- 告警有闩，不刷屏也不漏报，补货后重新武装（[[problems-coffee-machine-alert-latch]]）。
- 出口用资源池表示，并说得出这道题为什么不需要订单队列（[[problems-coffee-machine-outlets-as-resource-pool]]）。
- 原料名是开放的字符串键而不是枚举，并配上"不认识的原料算缺料"这条补偿（[[problems-coffee-machine-ingredients-are-data]]）。
- 并发测试用屏障断言不变式（不超卖、并发度恰好等于出口数），一句 `sleep` 都没有（[[problems-coffee-machine-concurrency-test]]）。
- 知道 `self._served += 1` 不是原子的，GIL 保护不了它（[[problems-coffee-machine-counter-not-atomic]]、[[concurrency-augmented-assignment-not-atomic]]）。
- 任何时刻最多持一把锁，因此不需要约定加锁顺序（[[problems-coffee-machine-one-lock-at-a-time]]）。
- 主动放弃 `Menu`、`Outlet` 和转发式的 `refill()`，并说得出判据是"它守着什么不变式"（[[problems-coffee-machine-refuse-forwarding-classes]]）。

**题解**：[[solution-coffee-machine]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
