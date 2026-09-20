%% trellis:begin %%
# 内存持久化（In-Memory Persistence）
*API 与程序结构（Program Structure）*

仓储（repository）模式、id 生成、二级索引，以及线程安全的内存存储。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/low-level-design/map/problems.machines.parking-lot|停车场（Parking Lot）]], [[domains/low-level-design/map/problems.machines.amazon-locker|快递柜（Amazon Locker）]], [[domains/low-level-design/map/problems.booking.movie-booking|电影订票（BookMyShow）]], [[domains/low-level-design/map/problems.booking.meeting-scheduler|会议室预订（Meeting Scheduler）]], [[domains/low-level-design/map/problems.marketplaces.online-shopping|在线购物（Amazon）]], [[domains/low-level-design/map/problems.marketplaces.stock-brokerage|股票交易系统（Stock Brokerage）]], [[domains/low-level-design/map/problems.marketplaces.bank-account|银行账户系统（Bank Account System）]], [[domains/low-level-design/map/problems.components.kv-store|内存键值存储（In-Memory Key-Value Store）]]

## Readings
- [[fowler-repository|Repository (Fowler, P of EAA catalog)]]
- [[msdocs-persistence-layer|Designing the Infrastructure Persistence Layer (Microsoft .NET Architecture)]]

## Drills
- [[design-amazon-locker|Drill：快递柜（Amazon Locker）]]
- [[design-bank-account|Drill：银行账户系统（Bank Account System）]]
- [[design-hotel-booking|Drill：酒店预订（Hotel Booking）]]
- [[design-kv-store|Drill：内存键值存储（In-Memory Key-Value Store）]]
- [[design-meeting-scheduler|Drill：会议室预订（Meeting Scheduler）]]
- [[design-movie-booking|Drill：电影订票（BookMyShow）]]
- [[design-online-shopping|Drill：在线购物（Online Shopping）]]
- [[design-parking-lot|Drill：停车场（Parking Lot）]]
- [[design-stock-brokerage|Drill：股票交易系统（Stock Brokerage）]]

## Cards (4)
1. [[structure-storage-repository-boundary]]
2. [[structure-storage-id-generation]]
3. [[structure-storage-secondary-index]]
4. [[structure-storage-chm-compound-ops]]
%% trellis:end %%

## Notes
