---
nodes: [problems.media.video-conferencing]
url: https://discord.com/blog/how-discord-handles-two-and-half-million-concurrent-voice-users-using-webrtc
---
# How Discord Handles Two and a Half Million Concurrent Voice Users using WebRTC
值得读：披露了真实的大规模媒体服务运营数字（260 万并发语音用户、850+ 台语音
服务器、13 个区域、220Gbps 出口流量），以及他们为简化架构完全放弃 ICE、强制
全部媒体走自建中继这一和标准 WebRTC 流程不同的真实取舍。本题解「容量估算」一节
用其"用户数/服务器"比例对自己算出的媒体服务器容量做方向性交叉验证；本题解按
标准 ICE 流程设计，与 Discord 放弃 ICE 的选择不同，「五分钟讲法」末尾点明了
这个分歧。
