---
id: delivery-canary-cohort
node: delivery.canary
type: qa
---
## Q
A cache change succeeds on 1% of globally random requests. Why may that canary miss the highest-risk failures?

## A
Random request sampling can spread one user's requests across policies, contaminate shared cache state, and underrepresent small regions, large objects, hot keys, or cold misses. Choose a stable isolation boundary—such as region, cache node, tenant, or deterministic key cohort—then ensure the cohort includes risky traffic classes. Canary design must preserve comparability without allowing experimental state to leak into control.

## Q zh
一个 cache change 在 global random 1% request 上成功。为什么这个 canary 仍可能漏掉最高风险的 failure？

## A zh
random request sampling 可能让同一用户的 request 分散到不同 policy、污染 shared cache state，并低估 small region、large object、hot key 或 cold miss。应选择 stable isolation boundary，例如 region、cache node、tenant 或 deterministic key cohort，并确保 cohort 包含高风险 traffic class。canary design 必须保持 comparability，同时阻止 experimental state 泄漏到 control。
