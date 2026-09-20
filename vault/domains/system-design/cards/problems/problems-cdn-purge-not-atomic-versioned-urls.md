---
id: problems-cdn-purge-not-atomic-versioned-urls
node: problems.foundations.cdn
type: qa
step: 4
tags: [grown]
---
## Q
In a CDN that propagates a purge request to all edge PoPs through a fan-out broadcast tree with a P99 target of under 2 seconds, why is it wrong to treat that 2-second budget as a guarantee that all users see either the old or the new content, never a mix - and what design choice avoids relying on that guarantee for content like prices?

## A
Purge propagation across physically distributed PoPs takes real, non-zero network time, so during that window different edge nodes in different regions have genuinely confirmed the purge at different moments - some serve the old cached copy, some already serve fresh content, which is a physical constraint of distributed broadcast, not an implementation bug. Content whose correctness depends on being read as either fully-new or fully-old (like a price) should not rely on purge speed at all: the fix is fingerprinted, immutable URLs (e.g. `product-42.v7.json`) - deploying a new version means publishing a new URL, which is an atomic, instantaneous swap at the page that references it, with no propagation window to reason about.

## Q zh
在一个 CDN 中，purge 请求通过广播树传递到所有边缘 PoP，P99 目标是 2 秒内。为什么把这个 2 秒预算当成「所有用户要么看到旧内容要么看到新内容、不会看到混合状态」的保证是错的？对于价格这类内容，什么设计选择能避免依赖这个保证？

## A zh
purge 在物理分布的 PoP 之间传播需要真实、非零的网络时间，所以在这段窗口内，不同区域的不同边缘节点确实会在不同时刻确认 purge——有些还在提供旧缓存，有些已经提供新内容，这是分布式广播的物理约束，不是实现缺陷。正确性依赖「要么完全新要么完全旧」的内容（如价格）不应该依赖 purge 速度：修复方法是指纹化、不可变的 URL（如 `product-42.v7.json`）——发布新版本变成发布一个新 URL，在引用它的页面上是原子、瞬时的切换，没有传播窗口需要考虑。
