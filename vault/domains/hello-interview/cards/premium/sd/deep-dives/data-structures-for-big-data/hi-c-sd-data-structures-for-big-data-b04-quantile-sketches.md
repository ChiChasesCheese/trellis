---
id: hi-c-sd-data-structures-for-big-data-b04-quantile-sketches
node: sd.deep-dives.data-structures-for-big-data.beyond
type: qa
step: 4
---
## Q
**大数据结构 · 拓展：固定桶之外的分位数结构**｜拓展 · 加分

固定边界的直方图有什么问题？t-digest、DDSketch 之类的结构怎么解决？

## A
- **固定桶的问题：** 边界要提前定好；分布变了或有离群值，桶就不合适；Prometheus 在桶内做线性插值，精度取决于桶落在哪。
- **相对误差：** 延迟类数据更关心「相对」误差（1ms 与 1.01ms 差不多，1s 与 1.01s 也一样）。DDSketch 用对数间距的桶，保证相对误差有界，如 1%。
- **t-digest：** 保存一组「质心与权重」，靠近两端（高分位）的质心更细、更准，中间合并得粗，所以对 p99、p99.9 更精确；也可合并。
- **取舍：** 固定桶最简单、最容易合并、最好做 SLO；t-digest/DDSketch 精度更好，实现更复杂。
- **面试说法：** 一般说直方图就够，被追问极端分位数的精度时，再提这两种。
