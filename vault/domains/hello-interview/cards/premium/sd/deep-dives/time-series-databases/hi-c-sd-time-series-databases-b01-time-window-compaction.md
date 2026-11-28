---
id: hi-c-sd-time-series-databases-b01-time-window-compaction
node: sd.deep-dives.time-series-databases.beyond
type: qa
step: 1
---
## Q
**时序数据库 · 拓展：按时间窗口压缩**｜拓展 · 加分

通用 LSM 的压缩策略（size-tiered、leveled）用在时序数据上有什么问题？Cassandra 的 TWCS 做了什么不同？

## A
- **问题：** 通用策略会把新旧数据混着合并，旧数据反复被重写，写放大高；设了 TTL 也很难让某个文件整体过期，要等合并才能清理。
- **TWCS 按时间窗口合并：** TWCS（Time Window Compaction Strategy）：按时间窗口分桶，同一窗口内的 SSTable 用 size-tiered 合并；窗口关闭后不再和别的窗口合并。
- **收益：** 同一文件的数据几乎同时过期，到期后整个 SSTable 直接删除，不需要重写。
- **前提：** 数据基本按时间顺序写入、只追加、很少更新。大量乱序或回填写入会让窗口反复被改动，收益消失。
- **模式。** 让物理布局与生命周期对齐：数据一起过期，就放在同一个文件里。
