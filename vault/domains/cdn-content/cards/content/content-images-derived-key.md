---
id: content-images-derived-key
node: content.images
type: qa
---
## Q
An image cache key contains only source URL and width. Users requesting AVIF and JPEG or different crop modes receive the wrong bytes. What must key identity include?

## A
Include a canonical source identity/version plus every transformation that changes output: width, height, fit/crop, quality, orientation policy, output format, and transformer version. Normalize equivalent inputs before hashing and bound allowed variants to avoid cardinality attacks. The response must emit matching `Content-Type` and `Vary` when format is negotiated from `Accept`.

## Q zh
image cache key 只有 source URL 和 width。请求 AVIF/JPEG 或不同 crop mode 的用户收到错误 bytes。key identity 必须包含什么？

## A zh
包含 canonical source identity/version，以及所有改变输出的 transformation：width、height、fit/crop、quality、orientation policy、output format 和 transformer version。hash 前 normalize 等价输入，并限制允许的 variant，避免 cardinality attack。若 format 由 `Accept` negotiation 得到，响应必须发出匹配的 `Content-Type` 和 `Vary`。
