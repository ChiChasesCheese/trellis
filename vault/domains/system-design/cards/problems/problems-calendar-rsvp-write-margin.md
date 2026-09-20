---
id: problems-calendar-rsvp-write-margin
node: problems.realtime.calendar
type: qa
step: 2
tags: [grown]
---
## Q
In a calendar design with 60 million daily active users, computed peak RSVP-write QPS (attendees responding to invitations) is about 2,083, using a x4 peak factor to reflect business-hours write concentration rather than the x3 used for globally-distributed read traffic. If a single relational primary is assumed to sustain a few thousand conditional updates/sec (about 3,000/sec), what is the safety margin, and what does it argue for in the attendee-state storage design?

## A
3,000 / 2,083 ≈ 1.44x — a thin margin, much thinner than a dating app's roughly 17.3x margin on its match-detection gate and close to the danger zone of a flash sale's roughly 1.8x margin on its single inventory key. This argues against writing all attendee RSVP updates to one global relational primary; attendee state should be sharded (e.g. by event id) across multiple relational primaries so each shard independently retains its own safety margin, rather than relying on a single primary at this write volume.

## Q zh
在一个 6000 万日活用户的日历设计里，算出的 RSVP 写入峰值 QPS（参会人回复邀请）约为 2,083，这里用了 ×4 的峰值系数来反映写操作在工作时段的集中，而不是读流量（全球分布）用的 ×3。如果假设单个关系型主库在简单条件更新下的承受能力是几千次/秒（约 3,000/秒），安全边际是多少？这对参会人状态的存储设计说明了什么？

## A zh
3,000 / 2,083 ≈ 1.44 倍——这是一个很薄的边际，比约会应用匹配判定网关约 17.3 倍的边际薄得多，接近秒杀设计里单一库存 key 约 1.8 倍边际的危险区间。这说明不应该把全部参会人 RSVP 状态更新都打向一个全局关系型主库；参会人状态应该（比如按事件 id）分片到多个关系型主库上，让每个分片各自独立保留自己的安全边际，而不是在这个写入量级下依赖单一主库。
