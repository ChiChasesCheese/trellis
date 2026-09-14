---
id: networking-dns-resolution-path
node: networking.dns
type: qa
---
## Q
Trace an uncached lookup of `api.example.com` from the browser to an answer. Where do caches sit in that path?

## A
Client stub resolver → **recursive resolver** (ISP or 8.8.8.8) which walks: **root** servers ("ask `.com`") → **TLD** servers ("ask example.com's nameservers") → **authoritative** server (returns the A/AAAA record).

Caches at every layer — browser, OS, recursive resolver — each honoring the record's **TTL**. In practice most lookups never leave the recursive resolver's cache, which is why DNS is fast and also why changes propagate slowly.

## Q zh
从浏览器跟踪一个未缓存的 `api.example.com` 查询到答案。缓存在该路径中的哪些位置？

## A zh
客户端存根解析器 → **递归解析器**（ISP 或 8.8.8.8）它遍历：**根**服务器（"询问 `.com`"）→ **TLD** 服务器（"询问 example.com 的名称服务器"）→ **权威**服务器（返回 A/AAAA 记录）。

每一层都有缓存 — 浏览器、OS、递归解析器 — 每个都遵守记录的 **TTL**。实际上大多数查询永远不会离开递归解析器的缓存，这就是 DNS 快速的原因，也是为什么更改传播缓慢的原因。
