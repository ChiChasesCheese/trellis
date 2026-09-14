---
id: net-setup-reuse
node: networking.dns-tcp-tls
type: qa
---
## Q
A proxy creates a fresh upstream TLS connection for every request. What production symptoms follow, and what is the safer design?

## A
You pay handshake RTT and cryptography per request, create ephemeral-port and FD pressure, lose congestion-window history, and may overload the origin with connection churn. Reuse a bounded keep-alive pool with sane idle/lifetime limits, validate certificates on creation, and monitor reuse rate, handshake rate, connection errors, and pool wait time.

## Q zh
proxy 每个请求都新建 upstream TLS connection。会出现什么生产症状？更安全的设计是什么？

## A zh
每次请求都要支付 handshake RTT 与 cryptography 成本，还会产生 ephemeral-port/FD pressure、丢失 congestion-window history，并可能用 connection churn 压垮 origin。使用有界 keep-alive pool，设置合理 idle/lifetime limit，建连时验证 certificate，并监控 reuse rate、handshake rate、connection error 与 pool wait time。
