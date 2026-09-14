---
id: net-http-representation
node: networking.http-semantics
type: qa
---
## Q
An origin sends Brotli bytes but omits `Content-Encoding: br`. Why can the CDN not safely infer the response from the filename?

## A
HTTP messages are self-describing: `Content-Type` identifies the media type and `Content-Encoding` identifies transformations applied to the representation. File extensions are not authoritative and intermediaries may not know origin storage conventions. Missing metadata causes clients to interpret compressed bytes as the media itself and can poison a shared cache.

## Q zh
origin 返回 Brotli bytes，却漏掉 `Content-Encoding: br`。为什么 CDN 不能靠 filename 安全推断响应？

## A zh
HTTP message 是 self-describing：`Content-Type` 标识 media type，`Content-Encoding` 标识对 representation 应用的 transformation。file extension 不具权威性，intermediary 也不了解 origin storage convention。metadata 缺失会让 client 把压缩字节当成媒体本身，还可能污染 shared cache。
