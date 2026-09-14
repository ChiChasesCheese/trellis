---
id: net-proxy-hop-headers
node: networking.proxies
type: qa
---
## Q
A reverse proxy forwards `Connection` and every header named by it to the upstream. What boundary is being violated?

## A
`Connection` identifies **hop-by-hop** fields that apply only to the current transport connection. A proxy must consume/remove them rather than forward them end-to-end; otherwise one peer can alter framing, persistence, or upgrade behavior on another hop. Reconstruct the upstream request from explicit policy, including `Host` and trusted forwarding metadata.

## Q zh
reverse proxy 把 `Connection` 以及它列出的所有 header 都转发给 upstream。违反了什么边界？

## A zh
`Connection` 标识只适用于当前 transport connection 的 **hop-by-hop** field。proxy 必须消费或删除它们，不能当作 end-to-end header 转发；否则一个 peer 可以改变另一 hop 的 framing、persistence 或 upgrade behavior。upstream request 应按明确 policy 重建，包括 `Host` 与可信 forwarding metadata。
