---
id: reliability-slos-user-centered-sli
node: reliability.slos
type: qa
---
## Q
A CDN's origin health check is green, but users in one region receive stale personalized pages. What should the availability SLI count, and why is origin uptime insufficient?

## A
Count eligible user requests that receive the correct representation within the promised latency. A fast but wrong or unauthorized response is bad, and the stale response is good only if the freshness contract explicitly permits it. Origin uptime measures a dependency, not the end-to-end user outcome across routing, cache selection, and delivery.

## Q zh
CDN 的 origin health check 是绿色，但某个 region 的用户收到 stale personalized page。availability SLI 应该如何计数，为什么 origin uptime 不够？

## A zh
应统计符合条件的 user request 中，在承诺 latency 内收到正确 representation 的比例。快速但错误或 unauthorized 的 response 仍是 bad event；只有 freshness contract 明确允许时，stale response 才算 good event。origin uptime 只测一个 dependency，没有覆盖 routing、cache selection 和 delivery 的端到端 user outcome。
