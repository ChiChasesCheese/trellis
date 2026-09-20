---
nodes: [problems.booking.hotel-booking, structure.state-machines, structure.storage]
tags: [problem]
---
# Drill：酒店预订（Hotel Booking）

一家连锁酒店集团：多个城市、每城几家店、每店上百间房分四种房型，对外开放未来 365 天的预订。
客人按城市 + 房型 + 日期区间搜索，下单、取消，到店入住、离店退房。照真实机考的节奏分关来做。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：建出酒店、房型、房间，以及一段入住日期区间；能按城市 + 房型 + 区间
  搜出有房的酒店，并下一笔预订。**先自己回答两个问题**：库存的计量单位是什么（一间房？一天？
  还是别的），以及客人订的到底是房型还是房号；这两个答案决定了后面所有代码的形状。
- 第 2 关（约 15 分钟）：把"这段日期还能订几间"算对，并让多晚预订的"查 + 订"**整段原子**——
  五晚里订到三晚是这道题的经典 bug。当场比较朴素的按晚计数表和线段树／区间树：按 365 天排期、
  一次住 1–5 晚，把两边各自要做多少次操作、多少行代码算出来再选，并说清结论在什么条件下反转。
- 第 3 关（约 15 分钟）：多人并发抢最后一间房；取消要把整段区间的库存还回去而且**只还一次**；
  入住与退房做成显式的状态机（预订 → 入住 → 退房，另有预订 → 取消）。用真线程加
  `threading.Barrier` 写测试，断言任何一晚都不超过实际房量。
- 第 4 关（选做）：加一条故意超卖（overbooking）的政策，或按夜动态定价（周末加价、剩余紧张时
  加价）。验收标准很硬：这两样加进来**不能改动按晚库存结构的任何一行**；还要说清超卖的代价在
  哪里兑现。

**怎么练**：把 `vault/domains/low-level-design/problems/hotel-booking/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/hotel-booking -q`。

**评分点**
- 库存单位定成"房型 × 一晚"，区间用半开的 `[check_in, check_out)`，退房当天不占用
  （[[problems-hotel-booking-night-is-the-unit]]）。
- 房号到入住时才绑定，说得出提前分房带来的碎片化与重排代价
  （[[problems-hotel-booking-late-room-assignment]]）。
- 数据结构的选择是算出来的，不是拍出来的：朴素计数表 vs 线段树，以及结论反转的条件
  （[[problems-hotel-booking-counter-vs-segment-tree]]）。
- 多晚预订是两段式（先全查、再全写）且两段在同一把锁里，不用"乐观写入再回滚"
  （[[problems-hotel-booking-range-reserve-atomic]]、[[concurrency-check-then-act]]）。
- "这段还能订几间"取区间内的最小值，不是首晚也不是平均
  （[[problems-hotel-booking-min-not-first]]）。
- 取消把计数减到 0 时直接删键、历史晚次有显式的清理路径，答得出"谁来删"
  （[[problems-hotel-booking-zero-bucket-deleted]]、[[structure-storage-repository-boundary]]）。
- 订单生命周期是一张显式转移表，取消的幂等性建在状态机的"认领"上
  （[[problems-hotel-booking-transition-table]]、[[structure-state-transition-table]]）。
- 超卖与动态定价是注入的普通函数，定价函数拿到的是被喂进去的剩余量而不是库存对象引用
  （[[problems-hotel-booking-overbooking-and-pricing]]）。

**题解**：[[solution-hotel-booking]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
