---
id: problems-video-conferencing-turn-relay-mandatory-fallback
node: problems.media.video-conferencing
type: qa
step: 4
tags: [grown]
---
## Q
In NAT traversal for video conferencing, why must a TURN relay fallback be treated as a mandatory, separately-provisioned tier of infrastructure rather than a rare edge case, and why does a relay server carry a lower effective participant capacity than a normal media-forwarding server with the same network interface?

## A
TURN must be mandatory because certain NAT type combinations (specifically address-dependent or address-and-port-dependent mapping on both sides, common behind restrictive corporate firewalls and some carrier-grade NATs) make hole-punching structurally impossible, not just unlikely — for that subset of participants, a relay is the only path that can ever work, not a fallback for occasional failures. A relay server has lower effective capacity per unit of network throughput because it must both receive and retransmit the exact same media bytes for every relayed participant — the same bytes consume network I/O budget twice (once in, once out) — roughly halving how many participants a relay server can serve compared to a normal forwarding node with identical NIC capacity.

## Q zh
在视频会议的 NAT 穿透设计里，为什么 TURN 中继回退必须被当作一层强制的、需要单独规划容量的基础设施，而不是罕见的边缘情况？为什么在相同网卡容量下，一台中继服务器的有效参会者承载能力比一台普通媒体转发服务器更低？

## A zh
TURN 之所以必须是强制的，是因为某些 NAT 类型组合（双方都是地址依赖或地址端口依赖映射，常见于限制性企业防火墙和部分运营商级 NAT 之后）会让打洞技术在协议层面上就不可能成功，而不只是「概率低」——对这部分参会者而言，中继是唯一能work的路径，而不是偶发失败时的兜底。中继服务器承载能力更低，是因为它必须为每个被中继的参会者同时接收和重新转发完全相同的媒体字节——同样的字节要消耗两次网络 I/O 预算（一次进、一次出）——在相同网卡容量下，能服务的参会者数量大约只有普通转发节点的一半。
