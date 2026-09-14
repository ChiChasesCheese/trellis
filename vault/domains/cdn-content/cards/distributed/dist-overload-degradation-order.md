---
id: dist-overload-degradation-order
node: distributed.overload
type: qa
---
## Q
A content service must degrade under overload. How should it decide what to shed first?

## A
Define an ordered degradation ladder before incidents: disable expensive optional transformations and personalization, serve stale or lower-quality variants, reject prefetch/bot/background traffic, then protect core public delivery. Admission should use cost and priority, not random arrival alone. Every step needs a measurable trigger, user-visible behavior, and recovery threshold. Graceful degradation is a product contract backed by capacity tests.

## Q zh
content service 在 overload 下必须 degrade。应如何决定先 shed 什么？

## A zh
incident 前定义有顺序的 degradation ladder：先关闭昂贵的 optional transformation 和 personalization，再服务 stale 或 lower-quality variant，随后 reject prefetch/bot/background traffic，最后保护核心 public delivery。admission 应按 cost 和 priority，而不只是随机到达。每一步都需要 measurable trigger、user-visible behavior 与 recovery threshold。graceful degradation 是由 capacity test 支撑的 product contract。
