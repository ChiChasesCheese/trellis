---
id: net-proxy-forward-vs-reverse
node: networking.proxies
type: qa
tags: [grown]
---
## Q
A company's employee laptops are configured to send every outbound request through `10.0.0.5`; a company's public website sends every inbound request through `10.0.0.9` before it reaches any application server. Which of these is a forward proxy and which is a reverse proxy, and what single question tells them apart?

## A
`10.0.0.5` is a **forward proxy**: the client (the laptop) is configured to know about it and chooses to route through it, typically to reach the wider internet on the client's behalf, hide the client's identity from servers, or enforce client-side policy such as content filtering. `10.0.0.9` is a **reverse proxy**: it sits in front of servers the client never sees or configures, accepting all inbound traffic and forwarding it to one of several backends; the client only ever knows the proxy's own address. The distinguishing question is: which side configured this hop, and which side does it hide? A forward proxy is chosen by, and hides, the client. A reverse proxy is deployed by, and hides, the servers.

## Q zh
一家公司的员工笔记本被配置为把所有出站请求都发往 `10.0.0.5`；这家公司的公开网站把所有入站请求先发往 `10.0.0.9`，再到任何 application server。哪一个是 forward proxy，哪一个是 reverse proxy？用哪一个问题就能把二者分开？

## A zh
`10.0.0.5` 是 **forward proxy**：client（笔记本）被配置为知道它的存在，并主动选择经它路由，通常是为了代表 client 访问更广的互联网、向 server 隐藏 client 的身份，或执行客户端策略（比如内容过滤）。`10.0.0.9` 是 **reverse proxy**：它部署在 client 从未见过也不会配置的一组 server 前面，接受所有入站流量并转发给若干 backend 之一；client 始终只知道这个 proxy 自己的地址。区分二者的问题是：这一跳是哪一方配置的，它又隐藏了哪一方？forward proxy 由 client 选择，隐藏的是 client；reverse proxy 由运维方部署，隐藏的是 server。
