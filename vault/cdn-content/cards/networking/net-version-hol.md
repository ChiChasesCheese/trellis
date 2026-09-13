---
id: net-version-hol
node: networking.http-versions
type: qa
---
## Q
How does head-of-line blocking differ between HTTP/1.1, HTTP/2, and HTTP/3 under packet loss?

## A
HTTP/1.1 avoids response interleaving, so browsers use multiple connections and a slow response blocks that connection. HTTP/2 multiplexes streams but all share one ordered TCP byte stream, so one lost packet stalls every stream. HTTP/3 maps streams onto QUIC; loss blocks only the affected stream, though congestion control still limits the whole connection.

## Q zh
在 packet loss 下，HTTP/1.1、HTTP/2、HTTP/3 的 head-of-line blocking 有什么不同？

## A zh
HTTP/1.1 不允许响应交错，因此 browser 使用多连接，而慢响应会阻塞所在连接。HTTP/2 multiplex 多个 stream，但都共享同一个有序 TCP byte stream，一个 packet 丢失会暂停所有 stream。HTTP/3 把 stream 映射到 QUIC，loss 只阻塞受影响 stream，但 congestion control 仍约束整个 connection。
