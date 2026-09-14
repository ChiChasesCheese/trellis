---
id: net-setup-rtt-budget
node: networking.dns-tcp-tls
type: qa
---
## Q
A first HTTPS request is slow but reused requests are fast. Which setup phases consume round trips, and what should you optimize before application code?

## A
The cold path can pay DNS resolution, a TCP handshake, and a TLS handshake before HTTP response work begins. Measure each phase separately. Prefer connection reuse, TLS 1.3/session resumption, a nearby edge, and HTTP/3 where loss makes TCP setup costly; do not attribute setup latency to the origin handler.

## Q zh
第一次 HTTPS 请求很慢，但复用连接后的请求很快。哪些 setup phase 消耗 RTT？优化 application code 前应该先做什么？

## A zh
cold path 在 HTTP 响应处理开始前，可能依次支付 DNS resolution、TCP handshake、TLS handshake。应分别测量各阶段。优先使用 connection reuse、TLS 1.3/session resumption、就近 edge，并在 packet loss 让 TCP setup 昂贵时考虑 HTTP/3；不要把 setup latency 归因给 origin handler。
