---
id: networking-connection-setup-cost
node: networking.protocols
type: cloze
---
A cold HTTPS request pays {{c1::1 RTT for the TCP handshake + 1 RTT for TLS 1.3}} before any application byte moves — on a 100 ms cross-region path that's ~200 ms of pure setup. This is why services use {{c2::keep-alive / connection pooling}} between fixed peers, and why QUIC offers {{c3::0-RTT resumption}} for repeat visitors.

## zh
冷 HTTPS 请求支付 {{c1::1 RTT 用于 TCP 握手 + 1 RTT 用于 TLS 1.3}}，然后任何应用字节才开始移动 — 在 100 ms 跨地域路径上这就是约 200 ms 的纯设置时间。这就是为什么服务在固定对等体之间使用 {{c2::keep-alive / 连接池}}，以及为什么 QUIC 为重复访问者提供 {{c3::0-RTT 恢复}}。
