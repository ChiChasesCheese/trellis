---
id: hi-c-sd-time-series-databases-x05-late-failure
node: sd.deep-dives.time-series-databases.exam
type: qa
step: 5
---
## Q
**时序数据库 · 预测失败：压缩收益消失**｜考点 · 必会

团队把「每次用户点击事件」当时序数据写入，时间戳不规律，数值是 64 位随机 ID，还带 `session_id` 标签。会发生什么？

## A
- **时间戳压缩失效：** delta-of-delta 依赖固定间隔；点击间隔不规律，差的差也是大数，要用更多比特。
- **值压缩失效：** XOR 依赖相邻值相似；随机 ID 异或后几乎全是有效位，压不动。
- **基数爆炸：** `session_id` 当标签，序列数等于会话数，内存索引撑爆。
- **结论：** 三个假设同时被打破，TSDB 比通用库还差。应改用事件日志加列式分析库（如 ClickHouse）或消息队列加数据湖。
- **高级表述：** 先说清数据假设，再选存储，而不是看到时间戳就选 TSDB。
