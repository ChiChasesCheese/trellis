---
id: networking-tls-resumption
node: networking.protocols
type: qa
---
## Q
TLS 1.3 session resumption: how do session tickets cut handshake cost, and why must 0-RTT early data be idempotent?

## A
After a full handshake the server issues an encrypted **session ticket**; on reconnect the client presents it as a pre-shared key — resuming without certificate exchange, and optionally sending application data **in the very first flight** (0-RTT).

0-RTT data is **replayable**: an attacker can capture that flight and re-send it, and the server can't tell — so only requests that are safe to execute twice (idempotent GETs) may ride 0-RTT; never mutations. Servers also rotate ticket keys, since a stolen ticket key retro-decrypts early data.

## Q zh
TLS 1.3 会话恢复：会话票如何切割握手成本，为什么 0-RTT 早期数据必须是幂等的？

## A zh
经过完整握手后，服务器发放一个加密的**会话票**；重连时客户端将其作为预共享键呈现 — 恢复而无需证书交换，并可选择在**非常第一个飞行中**发送应用数据（0-RTT）。

0-RTT 数据是**可重放的**：攻击者可以捕获该飞行并重新发送它，服务器无法区分 — 所以只有安全执行两次的请求（幂等 GET）可以乘坐 0-RTT；永远不变异。服务器也轮换票密钥，因为被盗的票密钥可以回溯解密早期数据。
