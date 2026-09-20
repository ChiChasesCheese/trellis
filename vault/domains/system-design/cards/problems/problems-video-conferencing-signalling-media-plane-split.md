---
id: problems-video-conferencing-signalling-media-plane-split
node: problems.media.video-conferencing
type: qa
step: 2
tags: [grown]
---
## Q
In a video conferencing system's architecture, why are the signalling plane (join/leave/mute control, carried over a persistent WebSocket) and the media plane (actual audio/video bytes, carried over UDP/SRTP) built as separate, decoupled systems rather than one unified service — and what failure-mode benefit does this decoupling produce?

## A
They're decoupled because their scaling and resource profiles are fundamentally different: signalling is lightweight control-plane traffic that a commodity long-connection gateway can handle at roughly 100K connections per machine, while media forwarding is bandwidth- and (for non-SFU architectures) CPU-intensive, requiring roughly two orders of magnitude more machines at the same concurrency. Decoupling them means an outage in the signalling gateway doesn't directly interrupt media already flowing between a client and its assigned media server — an in-progress call's audio and video keep working even if control operations like toggling mute or a new participant joining temporarily fail, because the media path never depended on the signalling connection staying up once it was established.

## Q zh
在一个视频会议系统架构里，为什么信令面（加入/离开/静音控制，走持久 WebSocket）和媒体面（真正的音视频字节，走 UDP/SRTP）要构建成两套互相解耦的独立系统，而不是一个统一的服务？这种解耦带来了什么故障模式上的好处？

## A zh
解耦的原因是两者的扩展性和资源特征本质不同：信令是轻量的控制面流量，普通商用长连接网关单机就能撑住约 10 万条连接；而媒体转发对带宽（以及非 SFU 架构下对 CPU）的消耗很大，同等并发量下所需机器数比信令面高出大约两个数量级。解耦之后带来的好处是：信令网关故障不会直接中断客户端和它所分配的媒体服务器之间已经在传输的媒体——即便静音切换、新人加入这类控制操作暂时失败，一场进行中通话的音视频仍能继续工作，因为媒体路径一旦建立就不再依赖信令连接持续存活。
