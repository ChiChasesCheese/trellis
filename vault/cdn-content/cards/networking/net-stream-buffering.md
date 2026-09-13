---
id: net-stream-buffering
node: networking.streaming
type: qa
---
## Q
A route is advertised as streaming, but TTFB equals the time to generate the entire body. Where should you look?

## A
Look for buffering at every boundary: application writer, compression middleware, reverse proxy, CDN, and client library. Confirm headers are flushed, chunks actually leave the process, intermediaries allow streaming, and transforms do not require the full body. Streaming is an end-to-end property; one buffering hop turns it back into batch delivery.

## Q zh
一个 route 宣称支持 streaming，但 TTFB 等于生成整个 body 的时间。应该查哪里？

## A zh
检查每个 boundary 的 buffering：application writer、compression middleware、reverse proxy、CDN、client library。确认 header 已 flush、chunk 确实离开进程、intermediary 允许 streaming，且 transformation 不要求完整 body。streaming 是 end-to-end property；任意一个 buffering hop 都会把它变回 batch delivery。
