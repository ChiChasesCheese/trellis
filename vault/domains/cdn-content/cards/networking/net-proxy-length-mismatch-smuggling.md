---
id: net-proxy-length-mismatch-smuggling
node: networking.proxies
type: qa
tags: [grown]
---
## Q
A single HTTP request arrives carrying both a `Content-Length` header and a `Transfer-Encoding: chunked` header. A front-end proxy frames the request body using one of these headers while the back-end server frames it using the other. What attack does this discrepancy enable, and what is the fix?

## A
**HTTP request smuggling.** If the proxy decides where the request ends using `Content-Length` while the upstream decides using `Transfer-Encoding` (or vice versa), the two hops disagree on which bytes belong to this request and which belong to the next one on the same connection. An attacker can craft bytes that the proxy treats as the tail of a harmless request but the upstream treats as the start of a second, smuggled request — bypassing whatever the proxy checked, because the proxy never saw that second request as a request. The fix is to reject any message carrying both headers outright, and to make the proxy and upstream agree on one framing mechanism (per HTTP semantics, `Transfer-Encoding` takes precedence when both are present and legal) rather than letting each hop parse independently.

## Q zh
一个 HTTP 请求同时带有 `Content-Length` header 和 `Transfer-Encoding: chunked` header。前端的 proxy 用其中一个 header 来判断 request body 的边界，后端 server 却用另一个来判断。这种分歧会带来什么攻击？该怎么修？

## A zh
**HTTP request smuggling（请求走私）。** 如果 proxy 用 `Content-Length` 判断请求在哪里结束，而 upstream 用 `Transfer-Encoding` 判断（或者反过来），这两跳就会对同一条连接上哪些字节属于这个请求、哪些属于下一个请求产生分歧。攻击者可以构造这样的字节：proxy 认为它们是一个无害请求的结尾，而 upstream 认为它们是第二个、被走私进来的请求的开头——从而绕过 proxy 做过的任何检查，因为 proxy 从未把那第二个请求识别成一个请求。修复方法是直接拒绝任何同时带有这两个 header 的报文，并让 proxy 与 upstream 就唯一一种 framing 机制达成一致（按 HTTP 语义，当两者同时出现且都合法时，`Transfer-Encoding` 优先），而不是让每一跳各自独立解析。
