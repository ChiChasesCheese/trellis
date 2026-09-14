---
id: client-redirect-not-instant-dns
node: continuity.client-redirect
type: qa
tags: [grown]
---
## Q
执行 `ALTER CONNECTION … PRIMARY` 后，为什么部分客户端仍会在一段时间内连到旧账户或报错？

## A
连接 URL 通过 DNS 解析到当前主连接所在的账户，切换主连接实质上是更新这个 DNS 记录。客户端和中间网络会缓存 DNS 结果，已经建立的会话也不会自动迁移，所以只有在缓存过期、客户端重新建立连接之后才会连到新账户。应用应当具备断线重连与重试逻辑，才能在切换时自动恢复。
