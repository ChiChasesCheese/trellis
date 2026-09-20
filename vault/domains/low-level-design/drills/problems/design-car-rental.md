---
nodes: [problems.booking.car-rental, patterns.strategy]
tags: [problem]
---
# Drill：租车系统（Car Rental）

一家连锁租车公司：几十个门店、几百辆车分四个车型档次，客人按小时下单、租期从几小时到几个月，
**支持异地还车**——在浦东机场取的车可以还到虹桥。这道题看起来和酒店预订是同一道，
所以最容易犯的错是把「(房型, 一晚) → 已订数」那套计数表直接搬过来。搬之前先回答一个问题：
**酒店的计数表凭什么成立？**（凭房间不会离开酒店。车会。）

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：车辆、车型、门店的建模；小时粒度的半开租期（不足一小时按一小时计费）；
  给定门店 + 车型 + 时段，查出还有哪些车能租；下一笔预约。动手之前先定一件事：**库存的单位
  是什么**——是「门店里的一辆车」，还是别的？这个选择在第 2 关会被当场兑现。
- 第 2 关（约 15 分钟）：支持异地还车。先自己构造一个反例：一辆 7 号从 A 开到 B 的车，10 号在 A
  有没有时间冲突？能不能租？把这个反例写成一条测试，再让代码通过它。然后回答：可用性判据里
  除了时间，还必须有什么？位置该**存**成字段还是**算**出来？为什么？
- 第 3 关（约 15 分钟）：取车与还车做成显式状态机（预约 / 已取车 / 已还车 / 已取消 / 爽约），
  外加三件现实失败：迟还五小时而这辆车十二点还有下一单、客人把车还到了约定之外的门店、
  还车时发现刮蹭要进厂 48 小时。写之前先问自己：这三件事是三个分支，还是同一件事？
  写完再回答一个只有异地还车才有的问题：**一辆车排了 A→B、B→C、C→A，第一段迟还挤掉了第二段，
  第三段会怎样？**
- 第 4 关（选做）：分项计费（车型 × 时长且长租封顶、异地附加费、保险加购、会员折扣按小计打），
  以及两个客人并发抢同一门店最后一辆车。判分点只有两个：加一项收费**不许动排期结构一行**；
  并发测试断言的是不变量（恰好一个成功、排期上恰好一段），不是时序。

**怎么练**：把 `vault/domains/low-level-design/problems/car-rental/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/car-rental -q`。

**评分点**
- 第一分钟就问「支不支持异地还车」，并说得出它为什么是全题的胜负手——可用性从此是一个位置问题，
  纯时间重叠判据直接错（[[problems-car-rental-availability-needs-location]]）。
- 可用性收敛成**一条**不变量（门店首尾相接 + 周转缓冲），可用性查询、迟还修复、维修封锁全部复用
  同一个判定函数，而不是三处各写一遍（[[problems-car-rental-one-invariant-chain]]）。
- 位置是沿着行程链**算出来**的纯函数，不是 `Vehicle` 上的 `current_branch` 字段，并说得出
  字段版为什么必然和链不一致（[[problems-car-rental-availability-needs-location]]、[[oop-entity-vs-value-object]]）。
- 说得出为什么租车必须在预约时就绑定车牌（早绑定），而酒店的房号要推迟到入住才分配（晚绑定）
  ——车有轨迹，房间没有（[[problems-car-rental-early-vs-late-binding]]）。
- 迟还、还错门店、事故进厂收敛成同一条「强行写入一段 + 修复时间轴」的路径，准点还车时这条路径
  什么也挤不掉（[[problems-car-rental-settle-unifies-three-failures]]）。
- 答得出挤占在异地还车下会**连锁**，并且说得清为什么同点还车时不会（[[problems-car-rental-displacement-cascades]]）。
- 行程链会缩，而且缩之前先把「车最后停在哪」吸收进起点——容器可以缩，不能连它承载的状态一起丢
  （[[problems-car-rental-purge-absorbs-location]]）。
- 「查可用 + 占车」是一个原子方法而不是两次调用，并说得出 GIL 给了什么、没给什么；并发测试用
  `Barrier` 对齐起跑、断言不变量（[[problems-car-rental-claim-is-one-call]]）。
- 计费是一串注入的纯函数而不是 `PricingStrategy` 抽象基类，签名里拿不到车队，返回分项而不是
  一个总数，金额用整数分（[[problems-car-rental-pricing-is-a-pipeline]]、[[patterns-strategy-callable]]）。
- 拒绝只有字段没有行为的 `Branch` 类、拒绝 `get_instance()` 单例，并说得出各自的判据
  （[[oop-getter-collection-leak]]）。

**题解**：[[solution-car-rental]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
