---
id: problems-video-conferencing-simulcast-tile-cap-bounds-downlink
node: problems.media.video-conferencing
type: qa
step: 5
tags: [grown]
---
## Q
An SFU that forwards every other participant's full-resolution stream to each receiver still has downlink bandwidth growing with N — at N=25 participants and 1.54 Mbps per stream, that's about 37 Mbps of downlink per receiver, which is infeasible for typical consumer bandwidth. What mechanism keeps SFU downlink bandwidth bounded regardless of meeting size, and roughly what downlink bandwidth does it produce?

## A
Senders encode simulcast layers (multiple independently-encoded quality tiers of the same video), and the SFU forwards only the layer each receiver actually needs based on what's visibly rendered on that receiver's screen — a high layer for whichever participant is shown large (e.g. the active speaker), and a thin, low-bitrate layer for the rest shown as thumbnails, rather than a full-resolution stream for every single other participant. Because a meeting UI only ever fully renders a small, bounded number of tiles regardless of how many people are in the call, downlink bandwidth is capped by that visible-tile limit rather than by N: for example, one active-speaker layer at 1.5 Mbps plus 24 thumbnail layers at 0.15 Mbps each comes to about 5.1 Mbps of downlink, largely independent of whether the meeting has 25 or 250 participants.

## Q zh
如果 SFU 对每个接收端都转发其余所有参会者的完整分辨率流，下行带宽仍会随 N 增长——N=25、每路流 1.54Mbps 时，每个接收端下行约需 37Mbps，对典型消费级带宽来说不可行。什么机制能让 SFU 的下行带宽不随会议规模增长？大致会产生多大的下行带宽？

## A zh
发送端把视频编码成多个独立的 simulcast 质量层，SFU 只根据接收端屏幕上实际渲染的内容，为每个接收端转发它真正需要的那一层——放大显示的参会者（比如当前发言人）转发高层，其余以缩略图形式展示的参会者转发低码率的薄层，而不是给每一个其他参会者都转发完整分辨率流。因为一个会议界面无论通话里有多少人，一次能完整渲染的画面格子数量本身就是有限且固定的，下行带宽因此被这个「可见画面数上限」卡住，而不是随 N 增长：比如一路发言人高层（1.5Mbps）加 24 路缩略图低层（各 0.15Mbps）合计约 5.1Mbps，基本不随会议是 25 人还是 250 人而变化。
