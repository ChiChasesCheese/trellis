---
id: content-rendering-mode-choice
node: content.rendering
type: qa
---
## Q
A product page is identical for most users, but inventory and cart are request-specific. Should the whole page use CSR, SSR, or static rendering?

## A
Do not make the whole route dynamic. Pre-render the shared shell and product content, then fetch or stream the inventory/cart behind explicit dynamic boundaries. Full SSR pays origin compute and TTFB on every request; full CSR delays meaningful content and ships more JavaScript. The correct unit of choice is the smallest data boundary whose freshness or personalization differs, not the entire page.

## Q zh
商品页对大多数用户相同，但库存和购物车是 request-specific。整页应该用 CSR、SSR 还是 static rendering？

## A zh
不要让整条 route 动态化。预渲染 shared shell 和商品内容，再通过显式 dynamic boundary 获取或 stream 库存与购物车。full SSR 每次请求都支付 origin compute 和 TTFB；full CSR 会延迟 meaningful content 并发送更多 JavaScript。正确选择单位是 freshness 或 personalization 不同的最小 data boundary，而不是整页。
