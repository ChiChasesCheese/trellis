---
id: problems-video-conferencing-cascaded-sfu-decouples-backbone-from-audience
node: problems.media.video-conferencing
type: qa
step: 8
tags: [grown]
---
## Q
For a 1000-person webinar with 5 presenters and viewers spread across 5 regions, sending every remote viewer's stream directly from one origin region costs that region about 7.46 Gbps of egress. With regional SFU cascading — presenter streams sent once to each of the other 4 regions, then fanned out locally within each region — what happens to inter-region backbone traffic, and why does that number not depend on audience size?

## A
With cascading, inter-region backbone traffic drops to just 4 remote regions x 5 presenter streams x 1.5 Mbps = 30 Mbps total — compared to 7.46 Gbps without it. This number doesn't depend on audience size because inter-region traffic now only carries one copy of each presenter's stream to each region, regardless of how many viewers are in that region; the audience-proportional traffic (995 viewers x their downlink bandwidth) still exists, but it happens entirely within each region's local network fan-out from that region's own SFU, not across the expensive long-haul backbone link. This is what decouples backbone cost from audience size: backbone traffic scales with (presenters x regions), local fan-out scales with (viewers per region), and only the first one is expensive per byte.

## Q zh
对于一场 1000 人的网络研讨会（5 位主讲人，观众分布在 5 个区域），如果每个远端观众都直接从源区域拉流，源区域出口带宽约需 7.46Gbps。如果改用区域级联 SFU——主讲人的流各向其余 4 个区域各发一份，再由每个区域本地扇出——跨区域骨干网流量会变成多少？为什么这个数字不随观众规模变化？

## A zh
采用级联后，跨区域骨干网流量降到仅 4 个远端区域 × 5 路主讲人流 × 1.5Mbps = 30Mbps——相比不做级联时的 7.46Gbps。这个数字之所以不随观众规模变化，是因为跨区域流量现在只需要把每位主讲人的流各送一份到每个区域，不管这个区域里有多少观众；和观众数量成正比的流量（995 名观众各自的下行带宽）依然存在，但它完全发生在每个区域内部、由该区域自己的 SFU 做本地扇出，不再经过昂贵的长途骨干链路。这正是让骨干网成本和观众规模解耦的机制：骨干网流量只随「主讲人数 × 区域数」增长，本地扇出才随「每区域观众数」增长，而只有前者的单字节成本才是昂贵的。
