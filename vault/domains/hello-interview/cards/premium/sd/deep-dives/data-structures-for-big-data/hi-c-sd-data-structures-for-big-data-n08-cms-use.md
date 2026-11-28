---
id: hi-c-sd-data-structures-for-big-data-n08-cms-use
node: sd.deep-dives.data-structures-for-big-data.notes
type: qa
step: 8
---
## Q
**大数据结构 · Count-Min Sketch 适用场景与坑**｜摘要 · 必会

Count-Min Sketch 怎么做 Top K 和缓存的 LFU？什么情况下不该用它？

## A
- **适用条件：** 要查计数；数据量大到存不下每个元素的计数；能容忍只会偏大的近似；要事先知道要查哪些元素，因为它不能告诉你里面有哪些元素。
- **Top K（如播放量前 K 的视频）：** 维护一个按计数排序的 K 个候选（有序列表或堆）；每次播放，在 sketch 里加一；加完查一次估计值，若它已在列表里就更新，或比列表最小的还大就换进去。
- **缓存 LFU：** 用 sketch 统计每个条目被访问的次数，配合堆记录最热的，不在榜上的是淘汰候选。
- **坑：** 系统别的部分依赖精确计数时，省下那点内存不值得；它本身仍要不少内存；通常得放宽需求才能用。
- **Redis 的做法：** 不用 Count-Min Sketch，而是复用每个键对象头里的 24 位字段：LRU 策略下存最近访问时间；LFU 策略下拆成 16 位最近衰减时间加 8 位对数计数器（近似频率）。
