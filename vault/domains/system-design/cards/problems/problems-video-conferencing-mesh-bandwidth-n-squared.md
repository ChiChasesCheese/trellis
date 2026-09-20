---
id: problems-video-conferencing-mesh-bandwidth-n-squared
node: problems.media.video-conferencing
type: qa
step: 1
tags: [grown]
---
## Q
In a video conferencing design where each participant's audio+video stream is a steady 1.54 Mbps, a full mesh topology (every participant connects directly to every other participant) requires each participant to simultaneously upload and download (N-1) x 1.54 Mbps. At N=6 participants, why does this already break down for a typical home broadband connection, and how does total network traffic across the whole mesh scale with N?

## A
At N=6, each participant needs about 7.70 Mbps of *simultaneous* upload and download just for media — the upload figure alone already exceeds or sits right at the upload cap of many consumer broadband plans, which are commonly asymmetric with upload capped well below download. Total network traffic across a full mesh scales with N^2 (every one of N participants sends to N-1 others), so unlike the other two architectures, doubling participant count more than quadruples aggregate network load — this is why mesh is only viable for very small calls (2-3 participants), never for anything approaching a typical multi-party meeting.

## Q zh
在一个视频会议设计里，假设每路参会者的音视频流稳定占用 1.54Mbps，全网状（mesh，每个参会者与其余所有参会者直连）拓扑要求每个参会者同时上传和下载 (N-1)×1.54Mbps。为什么 N=6 时这个方案对典型家庭宽带来说已经撑不住了？整个 mesh 网络的总流量随 N 如何增长？

## A zh
N=6 时，每个参会者需要约 7.70Mbps 的同时上传和下载带宽——仅上传这一项就已经逼近或超过许多消费级宽带套餐的上行上限，而这类套餐往往上下行不对称、上行远低于下行。整个 mesh 网络的总流量随 N² 增长（N 个参会者中每一个都要发给其余 N-1 个），这意味着和另外两种架构不同，参会人数翻倍会让总网络负载增长超过四倍——这正是 mesh 只适合 2-3 人的小型通话、无法用于任何接近典型多方会议规模场景的原因。
