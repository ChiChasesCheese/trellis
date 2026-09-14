---
id: security-request-integrity-hop-headers
node: security-cost.request-integrity
type: qa
---
## Q
Why must a reverse proxy parse the `Connection` header before forwarding request headers upstream?

## A
`Connection` can name additional hop-by-hop fields that apply only to the current transport link. Forwarding them can leak connection-specific state or let a client remove or reinterpret security-relevant headers at the next hop. Strip standard and nominated hop-by-hop fields, generate trusted forwarding metadata yourself, and test upgrade paths separately.

## Q zh
为什么 reverse proxy 在 forward request header 到 upstream 前，必须 parse `Connection` header？

## A zh
`Connection` 可以列出只适用于当前 transport link 的额外 hop-by-hop field。forward 它们可能泄漏 connection-specific state，或让 client 在下一 hop 删除、重新解释 security-relevant header。应移除标准和被点名的 hop-by-hop field，自行生成 trusted forwarding metadata，并单独测试 upgrade path。
