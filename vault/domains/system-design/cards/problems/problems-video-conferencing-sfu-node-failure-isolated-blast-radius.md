---
id: problems-video-conferencing-sfu-node-failure-isolated-blast-radius
node: problems.media.video-conferencing
type: qa
step: 7
tags: [grown]
---
## Q
When a single SFU node crashes in a video conferencing system that has split media forwarding across many independent SFU nodes, what happens to the participants assigned to that node, and why doesn't the failure affect participants on other SFU nodes even in the same meeting?

## A
Participants assigned to the crashed SFU node experience a visible interruption of a few seconds to tens of seconds: their client must perform an ICE restart, renegotiating connectivity and being reassigned to a healthy SFU node before media resumes. Participants on other SFU nodes are unaffected because media forwarding is deliberately partitioned across many independent nodes rather than concentrated in one giant central forwarder — each node's failure blast radius is limited to only the participants it was actively serving, which is the direct payoff of not building the media plane as a single scaled-up server.

## Q zh
在一个把媒体转发拆分到多个独立 SFU 节点的视频会议系统里，当某一个 SFU 节点崩溃时，分配到这个节点的参会者会发生什么？为什么这次故障不会影响同一场会议里其他 SFU 节点上的参会者？

## A zh
分配到崩溃节点的参会者会经历几秒到几十秒可感知的中断：客户端必须执行 ICE 重启，重新协商连通性并被分配到一个健康的 SFU 节点，之后媒体才恢复。其他 SFU 节点上的参会者不受影响，是因为媒体转发被有意拆分到多个互相独立的节点上，而不是集中在一个巨型的中心化转发器里——每个节点的故障影响范围被限制在它当时实际服务的那部分参会者，这正是不把媒体面做成单一超大服务器所带来的直接收益。
