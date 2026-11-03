---
id: hi-pt-url-shortener-design-2-code-length
node: qb.sd.url-shortener-design.points
type: qa
step: 2
---
## Q
**短链接服务 · 短码长度**｜必会 · 出自：短链接服务 › 需求

短码用 base62（0-9、a-z、A-Z）编码，要容纳 10 亿条短链接，应取 6 位还是 7 位？说出两者的组合数。

## A
**数字。** 7 位 62^7 约 3.5 万亿，6 位约 568 亿。
**为什么。** 6 位也够 10 亿条，但余量偏紧；7 位远大于 10 亿，是常用选择。
