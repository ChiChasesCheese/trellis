---
id: problems-chat-messaging-gateway-connection-capacity
node: problems.social.chat-messaging
type: qa
step: 1
tags: [grown]
---
## Q
In a WhatsApp-style chat system with 45 million peak concurrent WebSocket connections, why does that number — rather than messages-per-second — usually size the gateway (chat server) fleet, and what does a commodity stack assumption of about 100,000 connections per box imply for fleet size?

## A
Each gateway server holds WebSocket connections statefully, and a socket costs memory and file-descriptor state whether or not it is actively sending, so the fleet size tracks concurrent connections, not throughput. On a commodity stack (e.g. Go or Netty on Linux with epoll) a single box can typically hold about 100,000 concurrent WebSocket connections. At 45 million peak concurrent connections that requires roughly 450 gateway servers, plus about 30% headroom for multi-AZ redundancy and rolling deploys, landing around 600 boxes.

## Q zh
在一个类 WhatsApp 的聊天系统中，峰值有 4500 万并发 WebSocket 连接，为什么是这个数字（而不是每秒消息数）通常决定网关（chat server）机群的规模？商用栈假设单机约 10 万连接意味着需要多少台机器？

## A zh
每台网关服务器以有状态方式持有 WebSocket 连接，一个连接无论是否在发送数据都要占用内存和文件描述符状态，所以机群规模跟随并发连接数，而不是吞吐量。用商用栈（例如 Linux 上基于 epoll 的 Go 或 Netty）估算，单机通常能稳定维持约 10 万条并发 WebSocket 连接。在峰值 4500 万并发连接下，这需要约 450 台网关服务器，再加约 30% 的余量用于多可用区冗余和滚动发布，最终约 600 台。
