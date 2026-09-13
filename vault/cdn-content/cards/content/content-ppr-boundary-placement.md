---
id: content-ppr-boundary-placement
node: content.ppr
type: qa
---
## Q
Where should a PPR `Suspense` boundary sit around a personalized recommendation widget, and what happens if it wraps the whole page?

## A
Place it as close as possible around only the request-time subtree. The shared layout and product content stay in the cached static shell, while the fallback is sent immediately and the recommendation streams later. A boundary around the whole page turns the shell into a generic fallback, sacrificing pre-rendered content and TTFB value. Boundary placement is a cacheability and latency decision, not merely UI organization.

## Q zh
PPR 中 personalized recommendation widget 的 `Suspense` boundary 应放在哪里？如果它包住整页会怎样？

## A zh
应尽量贴近只需 request-time 的 subtree。shared layout 和商品内容保留在 cached static shell，fallback 立即发送，recommendation 稍后 stream。若 boundary 包住整页，shell 会退化成通用 fallback，丢失预渲染内容和 TTFB 价值。boundary placement 是 cacheability 与 latency 决策，不只是 UI 组织。
