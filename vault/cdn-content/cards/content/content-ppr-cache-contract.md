---
id: content-ppr-cache-contract
node: content.ppr
type: qa
---
## Q
Can a CDN cache the complete streamed PPR response that contains a user-specific cart? What representation should be cached instead?

## A
Not as one shared object: the final byte stream contains personalized data and would leak across users. Cache the static shell or framework-defined prerender artifact whose identity excludes request-specific holes; resolve and stream private holes per request. The platform contract must say which bytes are reusable and which are runtime output. Do not infer safety merely because the response began with static HTML.

## Q zh
CDN 能否缓存包含 user-specific cart 的完整 streamed PPR response？真正应该缓存什么 representation？

## A zh
不能把它作为一个 shared object：最终 byte stream 含 personalized data，会跨用户泄漏。应缓存 static shell 或 framework-defined prerender artifact，其 identity 不包含 request-specific hole；private hole 每次请求单独解析并 stream。平台 contract 必须明确哪些 bytes 可复用、哪些是 runtime output。不能因为响应开头是 static HTML 就推断整条响应安全。
