---
id: content-negotiation-encoding-layer
node: content.negotiation
type: qa
---
## Q
A response has `Content-Type: text/html` and `Content-Encoding: br`. What does each describe, and why must a cache keep them distinct?

## A
`Content-Type` describes the media representation after decoding; `Content-Encoding` describes the coding applied to transfer/store those bytes. Brotli and gzip variants are not different media types, but they are different byte representations with different validators and lengths. Cache them by normalized `Accept-Encoding` or separate variant keys, emit `Vary: Accept-Encoding`, and never label compressed bytes as a new content type.

## Q zh
响应包含 `Content-Type: text/html` 和 `Content-Encoding: br`。两者各描述什么，为什么 cache 必须区分？

## A zh
`Content-Type` 描述 decode 后的 media representation；`Content-Encoding` 描述传输或存储 bytes 时应用的 coding。Brotli/gzip variant 不是不同 media type，但确实是不同 byte representation，validator 和 length 也不同。应按 normalized `Accept-Encoding` 或独立 variant key 缓存，发送 `Vary: Accept-Encoding`，绝不能把 compressed bytes 标成新的 content type。
