---
id: security-economics-unit-cost
node: security-cost.economics
type: qa
---
## Q
Traffic doubled and the CDN bill rose 60%. Is that cost improvement or regression?

## A
Neither can be concluded without a unit. Track cost per delivered request, per successful GB, or per business-relevant object, segmented by region and cache outcome. Decompose transfer, edge requests, origin transfer, storage operations, compute, image transformation, and observability. Then compare unit cost and SLO together; lower unit cost achieved by serving worse content is not optimization.

## Q zh
traffic 翻倍，CDN bill 上升 60%。这是 cost improvement 还是 regression？

## A zh
没有 unit 无法判断。应跟踪每个 delivered request、每个 successful GB 或每个 business-relevant object 的成本，并按 region 与 cache outcome 切分。分解 transfer、edge request、origin transfer、storage operation、compute、image transformation 和 observability。然后同时比较 unit cost 与 SLO；靠提供更差 content 获得的更低 unit cost 不是 optimization。
