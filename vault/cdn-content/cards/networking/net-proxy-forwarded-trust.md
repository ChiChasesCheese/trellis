---
id: net-proxy-forwarded-trust
node: networking.proxies
type: qa
---
## Q
Why must an origin not blindly trust the leftmost `X-Forwarded-For` value?

## A
A client can send that header itself. Define trusted proxy hops, strip inbound forwarding headers at the edge, then append authenticated connection information. The origin should derive client identity using the known chain length or a standardized trusted-proxy policy; otherwise rate limits, geo policy, audit logs, and authorization can be spoofed.

## Q zh
为什么 origin 不能盲目信任 `X-Forwarded-For` 最左侧的值？

## A zh
client 自己也能发送这个 header。应定义 trusted proxy hop，在 edge 删除 inbound forwarding header，再追加经过认证的 connection information。origin 必须根据已知 chain length 或标准 trusted-proxy policy 推导 client identity；否则 rate limit、geo policy、audit log 与 authorization 都可能被伪造。
