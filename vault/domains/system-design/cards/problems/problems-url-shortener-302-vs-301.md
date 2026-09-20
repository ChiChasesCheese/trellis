---
id: problems-url-shortener-302-vs-301
node: problems.foundations.url-shortener
type: qa
step: 6
tags: [grown]
---
## Q
In a URL shortener design, why default to HTTP 302 (temporary redirect) instead of 301 (permanent redirect) for the short-code redirect response, given that 301 would let browsers and proxies cache the redirect and offload traffic from the origin?

## A
A 301 gets cached by browsers and intermediate proxies, so after the first visit a client never sends that request to the origin again — meaning the service loses the ability to later change the link's target, disable it (e.g., to take down a malicious link), or collect click analytics from that client. A 302 forces every visit to return to the origin, preserving control and analytics at the cost of the free traffic offload; 301 is only appropriate when the product guarantees a link's target will never change.

## Q zh
在一个短链接设计中，尽管 301（永久重定向）会被浏览器和代理缓存、从而为源站卸载流量，为什么重定向响应默认使用 302（临时重定向）而不是 301？

## A zh
301 会被浏览器和中间代理缓存，客户端第一次访问之后就再也不会把这个请求发回源站——这意味着服务失去了之后修改链接目标、下线链接（例如下架恶意链接）或者采集该客户端点击分析的能力。302 强制每次访问都回源，用放弃「免费的流量卸载」换取对链接的持续控制力和分析能力；只有当产品明确承诺某条链接的目标永不改变时，才适合用 301。
