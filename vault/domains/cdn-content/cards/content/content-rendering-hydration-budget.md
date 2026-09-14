---
id: content-rendering-hydration-budget
node: content.rendering
type: qa
---
## Q
Server rendering improves TTFB, but interaction remains slow because hydration blocks the main thread. What trade-off was missed?

## A
Fast HTML delivery does not guarantee fast interactivity. Hydration still downloads, parses, and executes client JavaScript. Keep noninteractive content as server-rendered components, isolate the smallest interactive islands, split code by route/component, and measure INP plus shipped JS—not only TTFB. CSR/SSR/SSG choose when HTML is produced; client-component boundaries determine how much browser work remains.

## Q zh
server rendering 改善了 TTFB，但 hydration 阻塞 main thread，交互仍很慢。漏掉了什么 trade-off？

## A zh
快速交付 HTML 不等于快速可交互。hydration 仍需下载、parse、执行 client JavaScript。把非交互内容保留为 server-rendered component，只隔离最小 interactive island，按 route/component 拆分代码，并测量 INP 和 shipped JS，而不只看 TTFB。CSR/SSR/SSG 决定 HTML 何时生成；client-component boundary 决定浏览器还剩多少工作。
