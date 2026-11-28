---
id: hi-c-sd-data-structures-for-big-data-x08-level-answer
node: sd.deep-dives.data-structures-for-big-data.exam
type: qa
step: 8
---
## Q
**大数据结构 · 中级与资深答案的差别**｜考点 · 必会

设计「统计全站每日独立访客」。中级与资深的回答各有什么特点？

## A
- **中级：** 每个用户 ID 放进 Redis 的 set，数 set 的大小，简单、正确。
- **资深加上的内容：**
  - 先算数据量：数亿用户的 set 要几十 GB，单机放不下；
  - 提出 HLL，一个键最多约 12 KB（Redis），误差约 1%，并说明 Redis 的 `PFADD/PFCOUNT` 直接可用；
  - 主动确认需求：业务能否容忍 1–2% 误差，若用于计费就不能；
  - 说明另一面：基数小的网页用 set 更简单精确。
- **关键：** 资深不是多说一个名词，而是说明为什么在这个规模换结构、牺牲什么、什么情况下不换。
