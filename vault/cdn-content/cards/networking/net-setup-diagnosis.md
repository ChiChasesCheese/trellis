---
id: net-setup-diagnosis
node: networking.dns-tcp-tls
type: qa
---
## Q
Only one geography sees intermittent connection setup failures. What evidence separates DNS, TCP, and TLS failures?

## A
Record DNS response/TTL and resolver errors; TCP connect time, retransmits and refused/timeouts; then TLS alert, negotiated version/cipher, SNI, certificate chain and expiry. Test from the affected network and POP. A single "connection failed" counter destroys the layer boundary needed to distinguish bad resolution, unreachable IPs, packet loss, and certificate/SNI mistakes.

## Q zh
只有一个 geography 间歇性 connection setup 失败。什么证据能区分 DNS、TCP 与 TLS failure？

## A zh
记录 DNS response/TTL 与 resolver error；TCP connect time、retransmit、refused/timeout；再记录 TLS alert、协商的 version/cipher、SNI、certificate chain 与 expiry。必须从受影响 network 和 POP 测试。单一“connection failed”计数器会抹掉 layer boundary，无法区分错误解析、IP 不可达、packet loss 与 certificate/SNI 错误。
