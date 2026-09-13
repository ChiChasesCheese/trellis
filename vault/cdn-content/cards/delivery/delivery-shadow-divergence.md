---
id: delivery-shadow-divergence
node: delivery.shadow
type: qa
---
## Q
Old and shadow cache implementations disagree on 0.2% of responses. What must be compared before deciding the shadow is wrong?

## A
Compare normalized decisions under the same inputs and point-in-time dependencies: cacheability, key components, selected representation, status, freshness, and body digest. Classify expected nondeterminism such as timestamps, race with revalidation, or dependency version; do not compare raw latency or bytes blindly. Review a production-shaped sample of every divergence class, especially any authorization or tenant boundary.

## Q zh
旧 cache implementation 与 shadow implementation 有 0.2% 的 response 不一致。在判断 shadow 错误前，必须比较什么？

## A zh
在相同 input 和 point-in-time dependency 下比较 normalized decision：cacheability、key component、selected representation、status、freshness 与 body digest。分类预期的 nondeterminism，例如 timestamp、与 revalidation 的 race 或 dependency version；不要盲目比较 raw latency 或 byte。对每类 divergence 抽取 production-shaped sample，尤其检查 authorization 或 tenant boundary。
