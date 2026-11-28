---
id: hi-c-sd-data-structures-for-big-data-b02-hll-merge
node: sd.deep-dives.data-structures-for-big-data.beyond
type: qa
step: 2
---
## Q
**大数据结构 · 拓展：HyperLogLog 的合并**｜拓展 · 加分

把 7 天的每日 HLL 合成一周的独立访客数，能做吗？交集呢？

## A
- **合并（并集）：** 可以，对应寄存器取最大值，得到的就是两个数据集并集的 HLL，结果与把所有元素直接放进一个 HLL 完全一致。Redis 里对应 `PFMERGE`。
- **为什么可以：** 寄存器记的是「见过的最大前导零数」，最大值本身可合并、可交换、与顺序无关。
- **交集：** 没有直接办法。可用容斥原理 |A∩B| = |A|+|B|−|A∪B|，但误差会叠加，交集小时相对误差很大，不可靠。
- **实际：** 每天存一个 HLL，每周、每月合并，就是常见的「预聚合加再汇总」；Redis 一个 HLL 固定约 12 KB，标准误差约 0.81%。
- **模式。** 可合并摘要：和分位数直方图一样，先压缩，再合并。
