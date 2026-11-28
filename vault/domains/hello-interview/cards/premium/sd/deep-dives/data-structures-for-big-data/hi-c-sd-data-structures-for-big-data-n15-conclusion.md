---
id: hi-c-sd-data-structures-for-big-data-n15-conclusion
node: sd.deep-dives.data-structures-for-big-data.notes
type: qa
step: 15
---
## Q
**大数据结构 · 小结：四个问题四种结构**｜摘要 · 必会

给你一个海量数据的统计需求，怎样一眼选出该用的数据结构？

## A
- **查成员：** 布隆过滤器，一定不在或可能在。
- **数次数：** Count-Min Sketch，次数上界，需要先知道要查谁。
- **数不同元素个数：** HyperLogLog，几 KB 估算数十亿的基数。
- **查分位数：** 直方图分桶，用桶宽换内存。
- **共同前提：** 能容忍一定误差，且数据大到精确做法不可行。这些结构展示深度，但用在不需要的地方就是过度设计。
