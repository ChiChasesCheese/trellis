---
nodes: [problems.booking.movie-booking, structure.storage, concurrency.primitives]
tags: [problem]
---
# Drill：电影订票（BookMyShow）

一家连锁院线：多个城市、每城几家影院、每家几个影厅、每厅每天十几场放映，一个影厅两三百个座。
热门首映开票的那一秒，同一场会有上万人同时点座。照真实机考的节奏分关来做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：建出城市 → 影院 → 影厅 → 场次 → 座位的层级；能列出某城某片的场次、
  查一场还剩哪些座、为选定的几个座下一笔订单。座位号不存在、座位已被占，都要抛明确的异常，
  不能返回 `None` 让调用方自己猜。**先想清楚"这个座位卖没卖掉"这份状态到底该挂在哪个对象上**，
  并准备好向面试官解释另外两个候选为什么被否掉。
- 第 2 关（约 15 分钟）：选座不等于成交。加一个带超时的锁座：`hold` → 付款后 `confirm` → 超时
  `expire` 并归还座位，三个状态显式可见。时钟必须是注入的——超时要能在**完全不 sleep** 的情况下
  测出来。想清楚超时是靠后台清扫兑现，还是每次读写时当场判断。
- 第 3 关（约 15 分钟）：很多用户并发抢同一场的同一批座位。用真线程加 `threading.Barrier` 写一个
  测试，断言：没有任何座位被卖两次；清扫之后没有任何座位卡在 HELD；三种状态的计数之和恒等于
  影厅座位数。说得出锁放在哪一层、为什么不是全局一把也不是一座一把，以及支付调用该在锁内还是锁外。
- 第 4 关（选做）：加按座位档次/排次定价、周末加价，再加一套分档退票政策（离开演越近退得越少）。
  验收标准很硬：这两样加进来**不能改动第 2、3 关写好的任何一行锁座与并发代码**。

**怎么练**：把 `vault/domains/low-level-design/problems/movie-booking/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/movie-booking -q`。

**评分点**
- 把座位分成物理层与场次层：`Seat` 不可变、被一个影厅的所有场次共用，"被谁占着"只属于 `Show`
  （[[problems-movie-booking-seat-two-layers]]）。
- 能把"谁持有锁座状态"的三个候选摆出来、说清全局锁座表的两份真源和无限增长的代价
  （[[problems-movie-booking-who-owns-hold-state]]）。
- 超时释放以惰性判断为准，清扫只做落实；测试里一次清扫都不调用也必须正确
  （[[problems-movie-booking-lazy-expiry]]）。
- 锁放在场次上，说得出"竞争边界和数据边界重合"，也说得出 GIL 为什么不能替掉这把锁
  （[[problems-movie-booking-lock-granularity]]、[[concurrency-gil-myth-invariants]]）。
- 支付调用在座位锁之外，并用"进支付窗口前在锁内延长持有期"补上那条缝
  （[[problems-movie-booking-payment-outside-lock]]、[[concurrency-lock-while-calling-out]]）。
- 一次锁多个座是全有或全无，检查与写入在同一把锁里完成
  （[[problems-movie-booking-all-or-nothing-hold]]、[[concurrency-check-then-act]]）。
- 订单不设 PENDING 状态——"已选座未付款"已经由锁座收据表达，不做第二份
  （[[problems-movie-booking-no-pending-status]]）。
- 定价与退票是注入的普通函数，加价格档和退票档位碰不到锁座机器
  （[[problems-movie-booking-policies-dont-touch-locks]]）。
- 每一个会增长的容器都答得出"什么条件下条目被移除"：场次目录靠清理已散场的场次收缩，座位表
  本身长度恒定（[[structure-storage-repository-boundary]]）。

**题解**：[[solution-movie-booking]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
