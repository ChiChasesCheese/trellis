---
id: networking-http2-vs-http3
node: networking.protocols
type: qa
---
## Q
HTTP/2 multiplexes many streams over one TCP connection. What problem remains, and how does HTTP/3 fix it?

## A
**TCP-level head-of-line blocking**: one lost packet stalls *every* HTTP/2 stream on that connection until retransmission, because TCP delivers bytes in order.

**HTTP/3 runs on QUIC (over UDP)**: loss recovery is per-stream, so a dropped packet stalls only its own stream. QUIC also folds the TLS handshake in (1-RTT, 0-RTT on resume) and survives client IP changes via connection IDs — big wins on lossy mobile networks.

## Q zh
HTTP/2 在一个 TCP 连接上多路复用许多流。什么问题仍然存在，HTTP/3 如何修复它？

## A zh
**TCP 级别的行首阻塞**：一个丢失的数据包停滞该连接上的*每个* HTTP/2 流，直到重传，因为 TCP 按顺序传递字节。

**HTTP/3 运行在 QUIC（通过 UDP）上**：损失恢复是每流的，所以一个丢弃的数据包只停滞其自己的流。QUIC 还折叠了 TLS 握手（1-RTT、恢复时 0-RTT）并通过连接 ID 存活客户端 IP 变更 — 在有损移动网络上的大赢。
