---
id: problems-video-conferencing-sfu-vs-mcu-compute-cost
node: problems.media.video-conferencing
type: qa
step: 3
tags: [grown]
---
## Q
Both an MCU (which fully decodes every incoming stream, composites them, and re-encodes) and an SFU (which forwards encoded packets without decoding) can serve a multi-party call, but they push cost onto completely different resources. For a 25-participant meeting with one shared composite view, assuming a CPU core can real-time decode about 12 streams but only encode about 4 (encoding is several times more expensive than decoding), roughly how many cores does the MCU's mixing alone cost, and why is an SFU's cost structurally much lower regardless of N?

## A
The MCU's mixing costs roughly 25/12 (decode) + 1/4 (one shared encode) ≈ 2.33 cores for this one meeting — and if personalized per-viewer layouts require a separate encode per participant instead of one shared composite, the encode term becomes 25/4 ≈ 6.25 cores, so cost scales with N on the encode side too. An SFU's cost is structurally lower because it never decodes or re-encodes media at all — it only inspects packet headers to make forwarding decisions, so its server-side cost is pure network I/O rather than compute-bound transcoding, roughly one to two orders of magnitude cheaper at the same participant count. This is why SFU is the default in modern products and MCU survives mainly as a legacy-interop gateway for endpoints that can't handle multiple simultaneous streams (e.g. PSTN/H.323 conference room hardware).

## Q zh
MCU（完整解码每一路输入流、合成后再重新编码）和 SFU（转发编码后的数据包、不解码）都能支撑多方通话，但两者把成本压在完全不同的资源上。对于一场 25 人会议、共享一路合成画面，假设一个 CPU 核心能实时解码约 12 路流、但只能实时编码约 4 路（编码比解码贵好几倍），MCU 单纯做混流大约需要多少核？为什么 SFU 的成本结构无论 N 多大都天然低得多？

## A zh
MCU 的混流大约需要 25/12（解码）+ 1/4（一路共享编码）≈ 2.33 核——如果需要千人千面的个性化布局、每个参会者单独编码而不是共享一路合成画面，编码这一项就变成 25/4≈6.25 核，说明编码侧的成本也会随 N 增长。SFU 的成本结构性更低，是因为它从不解码或重新编码媒体——只检查数据包头部就能做出转发决策，所以它的服务端成本是纯网络 I/O，而不是计算密集型的转码，同等参会人数下比 MCU 便宜一到两个数量级。这正是现代产品默认选择 SFU、而 MCU 主要作为兼容无法处理多路并发流的传统终端（比如 PSTN/H.323 会议室硬件）的遗留网关而存在的原因。
